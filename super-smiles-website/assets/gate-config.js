/* ------------------------------------------------------------------
   Booking gate configuration  —  THE ONE SWITCH
   ------------------------------------------------------------------
   This file is the single site-wide source of truth for "are bookings
   open?". It drives BOTH:
     · the announcement ticker above the nav on every page
     · which state /book renders (waitlist vs booking flow)

   ---- TO FLIP THE WHOLE SITE, EDIT ONE LINE ----------------------
   BOOKINGS_OPEN below:
     false  ->  bookings CLOSED  (amber ticker + waitlist on /book)
     true   ->  bookings OPEN    (brand ticker + booking flow)
     null   ->  decide automatically from the GATE_OPENS date
   -----------------------------------------------------------------

   Loaded in <head> on every page, BEFORE any content paints, so the
   correct state is on <html> from the first frame — no flash, no
   layout shift.

   NOTE: this site is static HTML with no server runtime, so the gate is
   evaluated in the browser and therefore reads the visitor's device
   clock. Fine for a marketing waitlist; not a security boundary.
   ------------------------------------------------------------------ */
(function (w, d) {
  "use strict";

  /* ---- the switch ---- */
  var BOOKINGS_OPEN = false;

  /* Used only when BOOKINGS_OPEN is null. Next intake: 12 Sep 2026, 9am AEST. */
  var GATE_OPENS = "2026-09-12T09:00:00+10:00";

  var opensAt = new Date(GATE_OPENS);
  var gateOpen = BOOKINGS_OPEN === null
    ? Date.now() >= opensAt.getTime()
    : BOOKINGS_OPEN === true;

  w.SuperSmilesGate = {
    GATE_OPENS: GATE_OPENS,
    BOOKINGS_OPEN: BOOKINGS_OPEN,
    opensAt: opensAt,
    gateOpen: gateOpen
  };

  /* Stamp state on <html> during head parse so CSS picks the right
     ticker treatment before first paint. */
  var root = d.documentElement;
  root.setAttribute("data-bookings", gateOpen ? "open" : "closed");

  /* Session-only dismiss (never permanent — someone who dismisses this
     must still get the explanation on their next visit). Read here, not
     later, so a dismissed bar is never painted and then removed. */
  try {
    if (w.sessionStorage && sessionStorage.getItem("ss-announce-dismissed") === "1") {
      root.setAttribute("data-announce", "dismissed");
    }
  } catch (e) { /* private mode / storage blocked — just show the bar */ }
})(window, document);
