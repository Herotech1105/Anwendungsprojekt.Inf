export function formatTimestampParts(ts) {
    const d = new Date(ts);

    const day = String(d.getDate()).padStart(2, "0");
    const month = String(d.getMonth() + 1).padStart(2, "0");
    const year = String(d.getFullYear()).slice(-2);

    const hours = String(d.getHours()).padStart(2, "0");
    const minutes = String(d.getMinutes()).padStart(2, "0");

    return {
        date: `${day}.${month}.${year}`,
        time: `${hours}:${minutes}`
    };
}

export function getTickIntervalMs(rangeHours) {
    if (rangeHours <= 1) {
        return 10 * 60 * 1000; // 10 Minuten
    }
    if (rangeHours <= 10) {
        return 2 * 60 * 60 * 1000; // 2 Stunden
    }
    if (rangeHours <= 24) {
        return 4 * 60 * 60 * 1000; // 4 Stunden
    }
    return null; // FROM–TO → auto
}
