// middleware - JWKS client configuration
const jwksClient = require('jwks-rsa');
const jwt = require('jsonwebtoken');

const KC_JWKS_URI = process.env.KC_JWKS_URI;
const KC_BASE_URL = process.env.KC_BASE_URL;
const https = require('https');
const fs = require('fs');

const client = jwksClient({
    jwksUri: KC_JWKS_URI,
    requestAgent: new https.Agent({
        ca: fs.readFileSync("certs/ca.crt"),
        rejectUnauthorized: true,
    }),
});

// retrieve signing key for JWT verification
const getKey = (header, callback) => {
    client.getSigningKey(header.kid, (err, key) => {
        if (err) {
            return callback(err);
        }
        const signingKey = key.getPublicKey();
        callback(null, signingKey);
    });
};


// middleware - authenticate token
const authenticateToken = (expectedAudience, requiredRole) => {
    return (req, res, next) => {
        const authHeader = req.headers.authorization || "";
        // check if the authorization header is present and starts with "Bearer "
        if (!authHeader.startsWith("Bearer ")) {
            return res.sendStatus(401);
        }

        // extract the token from the header
        const token = authHeader.split(" ")[1];
        // check if the token is provided
        if (!token) {
            return res.status(401).json({error: "No token provided"});
        }

        // options for token validation
        const validationOptions = {
            algorithms: ["RS256"],
            issuer: `${KC_BASE_URL}/realms/iot`,
        }
        // verify provided token
        jwt.verify(token, getKey, validationOptions, (err, decodedPayload) => {
            // if token verification fails, return 403 Forbidden
            if (err) {
                console.error("token verification failed");
                return res.status(403).json({
                    error: "Forbidden",
                    message: "Token verification failed (signature, expiration date or issuer invalid)."
                });
            }

            // retrieve the audience and authorized party from payload
            const aud = decodedPayload.aud;
            const azp = decodedPayload.azp;

            // check if the audience matches the expected audience
            const audienceOk =
                (azp === expectedAudience) ||
                (typeof aud === 'string' && aud === expectedAudience) ||
                (Array.isArray(aud) && aud.includes(expectedAudience));

            // if required audience is missing, return 403 Forbidden
            if (!audienceOk) {
                console.error(`Audience"${expectedAudience}" is missing`);
                return res.status(403).json({error: `Audience"${expectedAudience}" is missing`});
            }

            // retrieve roles from payload
            const roles = decodedPayload.realm_access?.roles || [];
            // check if required user role is provided
            if (requiredRole && !roles.includes(requiredRole)) {
                console.error(`Role ${requiredRole} is required`);
                return res.status(403).json({error: `Role ${requiredRole} is required`});
            }


            // continue if token is valid
            req.user = decodedPayload;
            next();
        });
    }
}

// middleware - authenticate API-key
const authenticateApiKey = (req, res, next) => {
    const apiKey = req.header('x-api-key');

    if (!apiKey || apiKey !== process.env.API_KEY) {
        return res.status(401).json({error: "Non authorised API-key"});
    }

    next();
};

module.exports = {authenticateToken, authenticateApiKey};