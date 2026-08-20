// 0FF THE PRINT — backend config.
//
// Paste your two values from Supabase (Project Settings -> API).
// Until you do, the site runs exactly as before on content/take.json.
//
// The anon key BELONGS in public web pages. Row Level Security is what protects
// the data, not secrecy of this key.
// NEVER put the service_role key here. It ignores every security rule.

window.OTP_SUPABASE = {
  url:     "",   // e.g. "https://abcdefgh.supabase.co"
  anonKey: "",   // the long "anon / public" key, starts with eyJ
};
