-- ─────────────────────────────────────────────────────────────────────────────
-- JanBaat — Row Level Security Policies
-- Run in: Supabase Dashboard → SQL Editor
-- Run AFTER: alembic upgrade head
-- ─────────────────────────────────────────────────────────────────────────────

-- ── Step 1: Enable RLS on all tables ─────────────────────────────────────────
ALTER TABLE profiles      ENABLE ROW LEVEL SECURITY;
ALTER TABLE posts         ENABLE ROW LEVEL SECURITY;
ALTER TABLE post_authors  ENABLE ROW LEVEL SECURITY;
ALTER TABLE poll_options  ENABLE ROW LEVEL SECURITY;
ALTER TABLE poll_votes    ENABLE ROW LEVEL SECURITY;
ALTER TABLE votes         ENABLE ROW LEVEL SECURITY;
ALTER TABLE comments      ENABLE ROW LEVEL SECURITY;
ALTER TABLE reports       ENABLE ROW LEVEL SECURITY;
ALTER TABLE notifications ENABLE ROW LEVEL SECURITY;
ALTER TABLE user_devices  ENABLE ROW LEVEL SECURITY;
ALTER TABLE ai_clusters   ENABLE ROW LEVEL SECURITY;

-- Location tables are public read-only (no sensitive data)
ALTER TABLE states    ENABLE ROW LEVEL SECURITY;
ALTER TABLE districts ENABLE ROW LEVEL SECURITY;
ALTER TABLE cities    ENABLE ROW LEVEL SECURITY;

-- ── Step 2: Auth trigger (create profile on signup) ───────────────────────────
CREATE OR REPLACE FUNCTION public.handle_new_user()
RETURNS trigger AS $$
BEGIN
  INSERT INTO public.profiles (id, phone)
  VALUES (new.id, new.phone)
  ON CONFLICT (id) DO NOTHING;
  RETURN new;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

DROP TRIGGER IF EXISTS on_auth_user_created ON auth.users;
CREATE TRIGGER on_auth_user_created
  AFTER INSERT ON auth.users
  FOR EACH ROW EXECUTE PROCEDURE public.handle_new_user();

-- ── Locations (public read, no write from client) ─────────────────────────────
CREATE POLICY "states_public_read"    ON states    FOR SELECT USING (true);
CREATE POLICY "districts_public_read" ON districts FOR SELECT USING (true);
CREATE POLICY "cities_public_read"    ON cities    FOR SELECT USING (true);

-- ── Profiles ──────────────────────────────────────────────────────────────────
CREATE POLICY "profiles_read_own"
  ON profiles FOR SELECT
  USING (auth.uid() = id);

CREATE POLICY "profiles_update_own"
  ON profiles FOR UPDATE
  USING (auth.uid() = id);

-- ── Posts (anyone can read active posts, only service_role writes) ────────────
CREATE POLICY "posts_public_read"
  ON posts FOR SELECT
  USING (status = 'active');

CREATE POLICY "posts_service_insert"
  ON posts FOR INSERT
  WITH CHECK (auth.role() = 'service_role');

CREATE POLICY "posts_service_update"
  ON posts FOR UPDATE
  USING (auth.role() = 'service_role');

-- ── Post Authors (CRITICAL: service_role only — protects anonymous identity) ──
CREATE POLICY "post_authors_service_only"
  ON post_authors FOR ALL
  USING (auth.role() = 'service_role');

-- ── Poll Options (public read, service_role write) ────────────────────────────
CREATE POLICY "poll_options_public_read"
  ON poll_options FOR SELECT
  USING (true);

CREATE POLICY "poll_options_service_write"
  ON poll_options FOR INSERT
  WITH CHECK (auth.role() = 'service_role');

CREATE POLICY "poll_options_service_update"
  ON poll_options FOR UPDATE
  USING (auth.role() = 'service_role');

-- ── Poll Votes ────────────────────────────────────────────────────────────────
CREATE POLICY "poll_votes_read_own"
  ON poll_votes FOR SELECT
  USING (auth.uid() = user_id);

CREATE POLICY "poll_votes_insert_own"
  ON poll_votes FOR INSERT
  WITH CHECK (auth.uid() = user_id);

CREATE POLICY "poll_votes_delete_own"
  ON poll_votes FOR DELETE
  USING (auth.uid() = user_id);

-- ── Votes ─────────────────────────────────────────────────────────────────────
CREATE POLICY "votes_read_all"
  ON votes FOR SELECT
  USING (true);

CREATE POLICY "votes_insert_own"
  ON votes FOR INSERT
  WITH CHECK (auth.uid() = user_id);

CREATE POLICY "votes_delete_own"
  ON votes FOR DELETE
  USING (auth.uid() = user_id);

-- ── Comments ──────────────────────────────────────────────────────────────────
CREATE POLICY "comments_read_all"
  ON comments FOR SELECT
  USING (true);

CREATE POLICY "comments_insert_own"
  ON comments FOR INSERT
  WITH CHECK (auth.uid() = user_id);

CREATE POLICY "comments_delete_own"
  ON comments FOR DELETE
  USING (auth.uid() = user_id);

-- ── Reports ───────────────────────────────────────────────────────────────────
CREATE POLICY "reports_insert_own"
  ON reports FOR INSERT
  WITH CHECK (auth.uid() = reporter_id);

CREATE POLICY "reports_read_service"
  ON reports FOR SELECT
  USING (auth.role() = 'service_role');

-- ── Notifications ─────────────────────────────────────────────────────────────
CREATE POLICY "notifications_read_own"
  ON notifications FOR SELECT
  USING (auth.uid() = user_id);

CREATE POLICY "notifications_update_own"
  ON notifications FOR UPDATE
  USING (auth.uid() = user_id);

CREATE POLICY "notifications_service_insert"
  ON notifications FOR INSERT
  WITH CHECK (auth.role() = 'service_role');

-- ── User Devices ──────────────────────────────────────────────────────────────
CREATE POLICY "user_devices_read_own"
  ON user_devices FOR SELECT
  USING (auth.uid() = user_id);

CREATE POLICY "user_devices_insert_own"
  ON user_devices FOR INSERT
  WITH CHECK (auth.uid() = user_id);

CREATE POLICY "user_devices_delete_own"
  ON user_devices FOR DELETE
  USING (auth.uid() = user_id);

-- ── AI Clusters (public read) ─────────────────────────────────────────────────
CREATE POLICY "ai_clusters_public_read"
  ON ai_clusters FOR SELECT
  USING (true);

CREATE POLICY "ai_clusters_service_write"
  ON ai_clusters FOR ALL
  USING (auth.role() = 'service_role');

