/* Resilient browser storage ----------------------------------------------
   A malformed value or blocked localStorage must never prevent UniRank from
   starting. All frontend features share this small defensive boundary. */
(function createUniStorage(global) {
  function read(key, fallback = null) {
    try {
      const value = global.localStorage.getItem(key);
      return value === null ? fallback : value;
    } catch (_) {
      return fallback;
    }
  }

  function write(key, value) {
    try {
      global.localStorage.setItem(key, String(value));
      return true;
    } catch (_) {
      return false;
    }
  }

  function remove(key) {
    try {
      global.localStorage.removeItem(key);
      return true;
    } catch (_) {
      return false;
    }
  }

  function readJSON(key, fallback = null) {
    const raw = read(key, null);
    if (raw === null) return fallback;
    try {
      return JSON.parse(raw);
    } catch (_) {
      remove(key);
      return fallback;
    }
  }

  function writeJSON(key, value) {
    try {
      return write(key, JSON.stringify(value));
    } catch (_) {
      return false;
    }
  }

  function readArray(key) {
    const value = readJSON(key, []);
    return Array.isArray(value) ? value : [];
  }

  function readObject(key) {
    const value = readJSON(key, null);
    return value && typeof value === 'object' && !Array.isArray(value) ? value : null;
  }

  global.uniStorage = Object.freeze({ read, write, remove, readJSON, writeJSON, readArray, readObject });
})(window);
