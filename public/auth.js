window.AUTH_MODE = 'demo';
/**
 * Auth & Profile System
 * Currently using "Local Demo Fallback" to simulate a real auth provider (like Supabase).
 */

const DEMO_USER_KEY = "unirank_demo_user";
const DEMO_PROFILE_KEY = "unirank_demo_profile";
const DEMO_PREFS_KEY = "unirank_demo_prefs";
const DEMO_FAVS_KEY = "unirank_demo_favs";

window.currentUser = null;
window.userProfile = null; // Basic profile + search preferences + interests
window.personalizationEnabled = false;

async function initAuth() {
  // Simulate restoring session
  const storedUser = localStorage.getItem(DEMO_USER_KEY);
  if (storedUser) {
    window.currentUser = JSON.parse(storedUser);
    await loadUserProfile();
  }
  
  // Sync personalization state
  const perfEnabled = localStorage.getItem("unirank_personalization_enabled");
  if (perfEnabled === "true" && window.userProfile) {
    window.personalizationEnabled = true;
  } else {
    window.personalizationEnabled = false;
  }
}

async function login(email, password) {
  // Simulated login
  window.currentUser = {
    id: "demo-uuid-1234",
    email: email,
    display_name: email.split("@")[0]
  };
  localStorage.setItem(DEMO_USER_KEY, JSON.stringify(window.currentUser));
  await loadUserProfile();
  return window.currentUser;
}

async function logout() {
  window.currentUser = null;
  window.userProfile = null;
  window.personalizationEnabled = false;
  localStorage.removeItem(DEMO_USER_KEY);
  localStorage.removeItem("unirank_personalization_enabled");
  // Don't remove profile/prefs from localstorage to simulate persistence across logouts for demo
}

async function loadUserProfile() {
  if (!window.currentUser) return null;

  const storedProfile = localStorage.getItem(DEMO_PROFILE_KEY);
  if (storedProfile) {
    window.userProfile = JSON.parse(storedProfile);
  } else {
    window.userProfile = null;
  }
  return window.userProfile;
}

async function saveUserProfile(profileData) {
  if (!window.currentUser) throw new Error("Must be logged in to save profile");
  
  // Simulated save
  window.userProfile = {
    ...window.userProfile,
    ...profileData,
    updated_at: new Date().toISOString()
  };
  localStorage.setItem(DEMO_PROFILE_KEY, JSON.stringify(window.userProfile));
  
  // Automatically enable personalization upon profile save
  setPersonalization(true);
  
  return window.userProfile;
}

function setPersonalization(enabled) {
  window.personalizationEnabled = enabled;
  localStorage.setItem("unirank_personalization_enabled", enabled ? "true" : "false");
  
  if (window.processAndRender) {
    window.processAndRender();
  }
}

async function addFavorite(programId) {
  if (window.currentUser) {
    let favs = JSON.parse(localStorage.getItem(DEMO_FAVS_KEY) || "[]");
    if (!favs.includes(programId)) {
      favs.push(programId);
      localStorage.setItem(DEMO_FAVS_KEY, JSON.stringify(favs));
    }
  }
}

async function removeFavorite(programId) {
  if (window.currentUser) {
    let favs = JSON.parse(localStorage.getItem(DEMO_FAVS_KEY) || "[]");
    favs = favs.filter(id => id !== programId);
    localStorage.setItem(DEMO_FAVS_KEY, JSON.stringify(favs));
  }
}

// Attach to window for global usage in script.js UI handlers
if (typeof window !== 'undefined') {
  window.initAuth = initAuth;
  window.login = login;
  window.logout = logout;
  window.loadUserProfile = loadUserProfile;
  window.saveUserProfile = saveUserProfile;
  window.setPersonalization = setPersonalization;
}
