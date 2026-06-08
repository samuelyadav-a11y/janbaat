export const POST_CATEGORIES = [
  "Roads",
  "Water",
  "Education",
  "Healthcare",
  "Corruption",
  "Jobs",
  "Safety",
  "Development",
  "Environment",
  "Other",
] as const;

export type PostCategory = (typeof POST_CATEGORIES)[number];

export const POST_FORMATS = ["text", "image", "poll"] as const;
export type PostFormat = (typeof POST_FORMATS)[number];

export const VOTE_TYPES = ["agree", "disagree", "metoo"] as const;
export type VoteType = (typeof VOTE_TYPES)[number];

export const FEED_LEVELS = ["district", "city", "state", "trending"] as const;
export type FeedLevel = (typeof FEED_LEVELS)[number];

export const POLL_MIN_OPTIONS = 2;
export const POLL_MAX_OPTIONS = 10;
export const POST_MAX_CHARS = 500;
export const COMMENT_MAX_CHARS = 300;
export const FEED_PAGE_SIZE = 20;
