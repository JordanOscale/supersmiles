/* ------------------------------------------------------------------
   Booking gate configuration
   ------------------------------------------------------------------
   GATE_OPENS is the moment public booking reopens.

     gateOpen === false  ->  /book renders the waitlist state
     gateOpen === true   ->  /book renders the normal booking flow

   The booking flow is never removed from the codebase — it lives in a
   <template> on book.html and is rendered back in when the gate opens.
   This gate is designed to open and close repeatedly: change the one
   date below and redeploy.

   NOTE: this site is static HTML with no server runtime, so the gate is
   evaluated in the browser and therefore reads the visitor's device
   clock. Fine for a marketing waitlist; not a security boundary.
   ------------------------------------------------------------------ */
(function (w) {
  "use strict";

  /* Next intake: 12 September 2026, 9:00am AEST (UTC+10). */
  var GATE_OPENS = "2026-09-12T09:00:00+10:00";

  var opensAt = new Date(GATE_OPENS);

  w.SuperSmilesGate = {
    GATE_OPENS: GATE_OPENS,
    opensAt: opensAt,
    gateOpen: Date.now() >= opensAt.getTime()
  };
})(window);
