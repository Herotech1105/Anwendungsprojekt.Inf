// main.js
import { initAuth } from "./auth.js";
import { initThemeToggle } from "./theme.js";
import { initEvents } from "./events.js";

console.debug("[main] initializing app");
initAuth();
initThemeToggle();
initEvents();
