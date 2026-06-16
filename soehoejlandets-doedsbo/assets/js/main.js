/* =========================================================================
   Søhøjlandets Dødsbo – interaktivitet
   - mobilmenu
   - FAQ-accordion
   - flertrins vurderingsformular med validering + indsendelse
   - kontaktformular
   ========================================================================= */
(function () {
  "use strict";

  /* ---- konfiguration: indsendelse af formularer -------------------------
     Sæt FORM_ENDPOINT til et Formspree/Make/webhook-endpoint, så sendes
     formularen direkte. Står den tom, åbnes brugerens mailprogram med en
     færdigudfyldt e-mail (mailto) som fallback, så siden virker uden backend. */
  var FORM_ENDPOINT = ""; // f.eks. "https://formspree.io/f/xxxxxxx"
  var CONTACT_EMAIL = "kontakt@shlb.dk";

  document.addEventListener("DOMContentLoaded", function () {
    initYear();
    initNav();
    initFaq();
    initWizard();
    initContactForm();
  });

  /* ---- år i footer ---- */
  function initYear() {
    document.querySelectorAll("[data-year]").forEach(function (el) {
      el.textContent = new Date().getFullYear();
    });
  }

  /* ---- mobilmenu ---- */
  function initNav() {
    var toggle = document.querySelector(".nav-toggle");
    var links = document.querySelector(".nav-links");
    if (!toggle || !links) return;
    toggle.addEventListener("click", function () {
      var open = links.classList.toggle("open");
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
    });
    links.querySelectorAll("a").forEach(function (a) {
      a.addEventListener("click", function () { links.classList.remove("open"); });
    });
  }

  /* ---- FAQ-accordion ---- */
  function initFaq() {
    document.querySelectorAll(".faq-item").forEach(function (item) {
      var q = item.querySelector(".faq-q");
      var a = item.querySelector(".faq-a");
      if (!q || !a) return;
      q.setAttribute("aria-expanded", "false");
      q.addEventListener("click", function () {
        var open = item.classList.toggle("open");
        q.setAttribute("aria-expanded", open ? "true" : "false");
        a.style.maxHeight = open ? a.scrollHeight + "px" : null;
      });
    });
  }

  /* ---- hjælpere til validering ---- */
  function markError(field, on) {
    if (!field) return;
    field.classList.toggle("invalid", !!on);
  }
  function isEmail(v) { return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v); }
  function isPhone(v) { return /^[\d +().-]{6,}$/.test(v); }

  function validateScope(scope) {
    var ok = true;
    scope.querySelectorAll("[required]").forEach(function (input) {
      var field = input.closest(".field") || input.closest(".choice-group");
      var val = (input.value || "").trim();
      var bad = false;
      if (input.type === "radio") {
        var group = scope.querySelectorAll('input[name="' + input.name + '"]');
        bad = ![].some.call(group, function (r) { return r.checked; });
        field = input.closest(".choice-group");
      } else if (input.type === "checkbox") {
        bad = !input.checked;
      } else if (!val) {
        bad = true;
      } else if (input.type === "email" && !isEmail(val)) {
        bad = true;
      } else if (input.type === "tel" && !isPhone(val)) {
        bad = true;
      }
      if (field) markError(field, bad);
      if (bad) ok = false;
    });
    return ok;
  }

  /* ---- flertrins vurderingsformular ---- */
  function initWizard() {
    var form = document.getElementById("vurderingForm");
    if (!form) return;

    var steps = [].slice.call(form.querySelectorAll(".fstep"));
    var dots = [].slice.call(form.querySelectorAll(".steps-bar .dot"));
    var btnPrev = form.querySelector("[data-prev]");
    var btnNext = form.querySelector("[data-next]");
    var btnSubmit = form.querySelector("[data-submit]");
    var current = 0;

    function show(i) {
      steps.forEach(function (s, idx) { s.classList.toggle("active", idx === i); });
      dots.forEach(function (d, idx) {
        d.classList.toggle("active", idx === i);
        d.classList.toggle("done", idx < i);
      });
      btnPrev.style.visibility = i === 0 ? "hidden" : "visible";
      btnNext.style.display = i === steps.length - 1 ? "none" : "inline-flex";
      btnSubmit.style.display = i === steps.length - 1 ? "inline-flex" : "none";
      if (i === steps.length - 1) buildSummary();
      window.scrollTo({ top: form.getBoundingClientRect().top + window.scrollY - 90, behavior: "smooth" });
    }

    btnNext.addEventListener("click", function () {
      if (!validateScope(steps[current])) return;
      if (current < steps.length - 1) { current++; show(current); }
    });
    btnPrev.addEventListener("click", function () {
      if (current > 0) { current--; show(current); }
    });

    // ryd fejl ved indtastning
    form.addEventListener("input", function (e) {
      var f = e.target.closest(".field"); if (f) f.classList.remove("invalid");
    });
    form.addEventListener("change", function (e) {
      var g = e.target.closest(".choice-group"); if (g) g.classList.remove("invalid");
    });

    function buildSummary() {
      var box = form.querySelector("#summary");
      if (!box) return;
      var data = collect(form);
      var rows = [
        ["Opgave", data.opgavetype],
        ["Boligtype", data.boligtype],
        ["Størrelse", data.stoerrelse ? data.stoerrelse + " m²" : ""],
        ["Ønsket tidspunkt", data.tidspunkt],
        ["Adresse på boet", data.boadresse],
        ["Navn", data.navn],
        ["Telefon", data.telefon],
        ["E-mail", data.email],
        ["Relation til afdøde", data.relation],
        ["Besked", data.besked]
      ].filter(function (r) { return r[1]; });
      box.innerHTML = rows.map(function (r) {
        return '<div style="display:flex;gap:12px;padding:8px 0;border-bottom:1px solid var(--line)">' +
          '<span style="min-width:170px;color:var(--muted)">' + r[0] + '</span>' +
          '<strong style="color:var(--ink);font-weight:600">' + escapeHtml(r[1]) + '</strong></div>';
      }).join("");
    }

    form.addEventListener("submit", function (e) {
      e.preventDefault();
      if (!validateScope(steps[current])) return;
      submitForm(form, "Vurderingsanmodning – Søhøjlandets Dødsbo", btnSubmit);
    });

    show(0);
  }

  /* ---- kontaktformular ---- */
  function initContactForm() {
    var form = document.getElementById("kontaktForm");
    if (!form) return;
    form.addEventListener("input", function (e) {
      var f = e.target.closest(".field"); if (f) f.classList.remove("invalid");
    });
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      if (!validateScope(form)) return;
      submitForm(form, "Henvendelse via kontaktformular – Søhøjlandets Dødsbo",
        form.querySelector('[type="submit"]'));
    });
  }

  /* ---- fælles indsendelse ---- */
  function collect(form) {
    var data = {};
    [].forEach.call(form.elements, function (el) {
      if (!el.name) return;
      if (el.type === "radio" || el.type === "checkbox") {
        if (el.checked) data[el.name] = el.value === "on" ? "Ja" : el.value;
      } else {
        data[el.name] = (el.value || "").trim();
      }
    });
    return data;
  }

  function submitForm(form, subject, btn) {
    var data = collect(form);
    var origLabel = btn ? btn.textContent : "";
    if (btn) { btn.disabled = true; btn.textContent = "Sender …"; }

    function done() {
      var card = form.closest(".form-card") || form.parentNode;
      var success = card.querySelector(".form-success");
      if (success) {
        form.style.display = "none";
        success.classList.add("show");
        window.scrollTo({ top: card.getBoundingClientRect().top + window.scrollY - 90, behavior: "smooth" });
      } else {
        alert("Tak! Vi har modtaget din henvendelse og vender hurtigt tilbage.");
      }
    }

    if (FORM_ENDPOINT) {
      fetch(FORM_ENDPOINT, {
        method: "POST",
        headers: { "Accept": "application/json", "Content-Type": "application/json" },
        body: JSON.stringify(Object.assign({ _subject: subject }, data))
      }).then(function (r) {
        if (!r.ok) throw new Error("fejl");
        done();
      }).catch(function () {
        mailtoFallback(subject, data);
        done();
      }).finally(function () {
        if (btn) { btn.disabled = false; btn.textContent = origLabel; }
      });
    } else {
      mailtoFallback(subject, data);
      if (btn) { btn.disabled = false; btn.textContent = origLabel; }
      done();
    }
  }

  function mailtoFallback(subject, data) {
    var lines = Object.keys(data).map(function (k) {
      return labelFor(k) + ": " + data[k];
    });
    var body = "Hej Søhøjlandets Dødsbo,%0D%0A%0D%0A" +
      "Jeg vil gerne høre nærmere. Her er mine oplysninger:%0D%0A%0D%0A" +
      encodeURIComponent(lines.join("\n")) +
      "%0D%0A%0D%0AVenlig hilsen";
    var href = "mailto:" + CONTACT_EMAIL + "?subject=" + encodeURIComponent(subject) + "&body=" + body;
    window.location.href = href;
  }

  function labelFor(key) {
    var map = {
      opgavetype: "Opgave", boligtype: "Boligtype", stoerrelse: "Størrelse (m²)",
      tidspunkt: "Ønsket tidspunkt", boadresse: "Adresse på boet", navn: "Navn",
      telefon: "Telefon", email: "E-mail", relation: "Relation til afdøde",
      besked: "Besked", samtykke: "Samtykke"
    };
    return map[key] || key;
  }

  function escapeHtml(s) {
    return String(s).replace(/[&<>"']/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c];
    });
  }
})();
