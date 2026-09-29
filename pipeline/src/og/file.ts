/**
 * The one name for a Shipped. OG card file. The generator writes it and the
 * issue renderer links it, so the two can never drift apart again (they did:
 * render linked og-v4.png while the generator wrote og.png, and issues 03-10
 * shipped with share images that 404ed). Bump the version to bust caches.
 */
export const OG_FILE = 'og-v5.png';
export const ogUrl = (issueNum?: string): string =>
  issueNum ? `https://id8labs.app/shipped/${issueNum}/${OG_FILE}` : `https://id8labs.app/shipped/${OG_FILE}`;
