/* 0FF THE PRINT — shared auth + posting helpers.
   Loaded by /join/, /compose/, /desk/ and the timeline on the homepage.
   Everything degrades quietly when the backend is not configured yet. */
(function (w) {
  const CFG = w.OTP_SUPABASE || {};
  const READY = !!(CFG.url && CFG.anonKey);

  let client = null;
  function sb() {
    if (!READY) return null;
    if (!client) {
      if (!w.supabase || !w.supabase.createClient) return null;
      client = w.supabase.createClient(CFG.url, CFG.anonKey);
    }
    return client;
  }

  const OTP = {
    configured: READY,
    sb,

    async me() {
      const c = sb(); if (!c) return null;
      const { data: { user } } = await c.auth.getUser();
      if (!user) return null;
      const { data: profile } = await c
        .from("profiles")
        .select("id, display_name, card_slug, approved, is_admin")
        .eq("id", user.id)
        .single();
      return { user, profile: profile || null };
    },

    async signUp(email, password, displayName, cardSlug) {
      const c = sb(); if (!c) throw new Error("Backend not configured yet.");
      const { data, error } = await c.auth.signUp({
        email, password,
        options: { data: { display_name: displayName, card_slug: cardSlug } },
      });
      if (error) throw error;
      return data;
    },

    async signIn(email, password) {
      const c = sb(); if (!c) throw new Error("Backend not configured yet.");
      const { data, error } = await c.auth.signInWithPassword({ email, password });
      if (error) throw error;
      return data;
    },

    async signOut() {
      const c = sb(); if (!c) return;
      await c.auth.signOut();
    },

    /* ---- posting ---- */
    async uploadImage(file) {
      const c = sb(); if (!c) throw new Error("Backend not configured yet.");
      const ext = (file.name.split(".").pop() || "jpg").toLowerCase();
      const name = `${Date.now()}-${Math.random().toString(36).slice(2, 8)}.${ext}`;
      const { error } = await c.storage.from("posts").upload(name, file, {
        cacheControl: "3600", upsert: false,
      });
      if (error) throw error;
      return c.storage.from("posts").getPublicUrl(name).data.publicUrl;
    },

    async post({ text, imageUrl, imageAlt }) {
      const c = sb(); if (!c) throw new Error("Backend not configured yet.");
      const { data: { user } } = await c.auth.getUser();
      if (!user) throw new Error("Log in first.");
      const { error } = await c.from("posts").insert({
        author_id: user.id,
        text: text.replace(/—/g, ","),   // em-dash reads as AI in the house voice
        image_url: imageUrl || null,
        image_alt: imageAlt || null,
      });
      if (error) throw error;
    },

    /* ---- the public feed ---- */
    async feed(limit = 60) {
      const c = sb(); if (!c) return [];
      const { data, error } = await c
        .from("feed").select("*").limit(limit);
      if (error) { console.warn("feed unavailable:", error.message); return []; }
      return (data || []).map(r => ({
        author: r.card_slug || "",
        author_name: r.display_name,
        text: r.text,
        image: r.image_url || "",
        image_alt: r.image_alt || "",
        pinned: !!r.pinned,
        date: r.created_at,
        live: true,
      }));
    },

    /* ---- admin ---- */
    async pending() {
      const c = sb(); if (!c) return [];
      const { data } = await c.from("profiles")
        .select("id, display_name, card_slug, approved, created_at")
        .eq("approved", false)
        .order("created_at", { ascending: false });
      return data || [];
    },

    async members() {
      const c = sb(); if (!c) return [];
      const { data } = await c.from("profiles")
        .select("id, display_name, card_slug, approved, is_admin, created_at")
        .eq("approved", true)
        .order("created_at", { ascending: false });
      return data || [];
    },

    async setApproved(id, approved) {
      const c = sb(); if (!c) throw new Error("Backend not configured yet.");
      const { error } = await c.from("profiles").update({ approved }).eq("id", id);
      if (error) throw error;
    },

    async pullPost(id) {
      const c = sb(); if (!c) throw new Error("Backend not configured yet.");
      const { error } = await c.from("posts").update({ published: false }).eq("id", id);
      if (error) throw error;
    },

    async allPosts(limit = 100) {
      const c = sb(); if (!c) return [];
      const { data } = await c.from("posts")
        .select("id, text, created_at, published, author_id, profiles(display_name)")
        .order("created_at", { ascending: false }).limit(limit);
      return data || [];
    },
  };

  w.OTP = OTP;
})(window);
