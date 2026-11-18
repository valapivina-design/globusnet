/* Portable review-comments injector.
 *
 * Drop on any static review site:
 *   1. Set CONFIG below (brand, Formcarry URL, path matcher, asset paths)
 *   2. Include comments.css
 *   3. Load comments data as window.SITE_COMMENTS = { "slug": [ ... ] }
 *   4. Load this file on review pages (or sitewide; it no-ops off-match)
 *
 * Data shape per comment:
 *   { name, initials, country, date:"YYYY-MM-DD", title, text, lang,
 *     askHelp?, importantLoss?, support?: { date, text, ctaLabel, ctaHref } }
 */
(function () {
  'use strict';

  var CONFIG = {
    brandName: 'GlobusNet',
    brandInitials: 'GN',
    commentsGlobal: 'SITE_COMMENTS',
    commentsScriptSrc: '../js/comments.js',
    formAction: 'https://formcarry.com/s/cxJd01H31MD',
    contactHref: '../pages/contact.html',
    privacyHref: '../pages/about.html',
    leadSource: 'review-comment',
    reviewPathRe: /\/reviews\/.+-review\.html$/i,
    insertBeforeSelectors: [
      'section.cta-section',
      'footer',
      '#footer-placeholder'
    ]
  };

  var UI = {
    heading: 'Comments & What Readers Are Saying',
    lead: 'Comments from people describing problems with {topic}. Our team may reply when the reported loss appears material and a confidential consultation could help. <a href="#submit-for-review">Submit for review</a> - all new submissions are moderated before publishing.',
    empty: 'No public comments published for this profile yet.',
    formHeading: 'Leave a comment',
    formLead: 'Share your experience with {topic}. <strong>All comments are moderated</strong> before anything is published. Email and phone are used only to follow up if needed and are <strong>never published</strong>.',
    name: 'Name',
    email: 'Email',
    phone: 'Phone',
    notPublished: '(not published)',
    subject: 'Subject',
    comment: 'Comment',
    namePh: 'Your name',
    emailPh: 'you@example.com',
    phonePh: 'Phone number',
    subjectPh: 'Brief subject line',
    bodyPh: 'Describe what happened. Include the domain you used if you can.',
    countryCode: 'Country code',
    privacy: 'By submitting, you agree we may contact you about this report. We decide which comments go live after review. See our <a href="{privacy}">Privacy Policy</a>.',
    submit: 'Submit comment',
    sending: 'Sending…',
    thanks: 'Thank you. Your comment was received and will be moderated before it appears live.',
    errSubmit: 'We could not submit that comment. Please try again in a moment.',
    errNetwork: 'No response from the form service. Please try again.',
    supportRole: 'Support',
    ctaFallback: 'Book a free consultation →',
    gotcha: 'Leave blank'
  };

  function escapeHtml(s) {
    return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
  }
  function escapeAttr(s) {
    return escapeHtml(s).replace(/'/g, '&#39;');
  }

  function getContext() {
    var path = window.location.pathname || '';
    if (!CONFIG.reviewPathRe.test(path)) return null;
    var file = (path.split('/').pop() || '').replace(/\.html$/i, '');
    var named = document.querySelector('[data-company]');
    var topic = named ? (named.getAttribute('data-company') || '') : '';
    if (!topic) {
      var h1 = document.querySelector('.page-hero h1, h1');
      var raw = (h1 ? h1.textContent : file).replace(/\s+/g, ' ').trim();
      var m = raw.match(/^Is\s+(.+?)\s+a\s+Scam\?/i);
      if (m) topic = m[1].trim();
      else topic = raw.replace(/\s*Review\s*$/i, '').trim();
    }
    topic = topic || file.replace(/-review$/i, '').replace(/-/g, ' ');
    return { slug: file, topic: topic };
  }

  function formatDate(iso) {
    try {
      return new Date(iso + 'T12:00:00').toLocaleDateString('en-GB', {
        day: 'numeric', month: 'short', year: 'numeric'
      });
    } catch (e) {
      return iso || '';
    }
  }

  function findInsertBefore() {
    for (var i = 0; i < CONFIG.insertBeforeSelectors.length; i++) {
      var el = document.querySelector(CONFIG.insertBeforeSelectors[i]);
      if (el) return el;
    }
    return null;
  }

  function insertNode(node, afterEl) {
    var before = afterEl ? afterEl.nextSibling : null;
    var anchor = findInsertBefore();
    if (afterEl && afterEl.parentNode) {
      if (before) afterEl.parentNode.insertBefore(node, before);
      else afterEl.parentNode.appendChild(node);
      return;
    }
    if (anchor && anchor.parentNode) anchor.parentNode.insertBefore(node, anchor);
    else document.body.appendChild(node);
  }

  function injectPublished(ctx) {
    if (document.getElementById('reviews-grid')) return;
    var db = window[CONFIG.commentsGlobal] || {};
    var items = db[ctx.slug] || [];

    var block = document.createElement('div');
    block.className = 'reviews-block';
    block.id = 'public-comments';

    var cards = '';
    if (!items.length) {
      cards = '<p class="reviews-empty-soft">' + escapeHtml(UI.empty) + '</p>';
    } else {
      for (var i = 0; i < items.length; i++) {
        var c = items[i];
        if ((c.name || '').toLowerCase().indexOf('trustpilot') !== -1) continue;
        if ((c.title || '').toLowerCase().indexOf('trustpilot') !== -1) continue;
        var lang = c.lang || 'en';
        cards += '<article class="review-card" lang="' + escapeAttr(lang) + '">' +
          '<div class="review-meta"><time datetime="' + escapeAttr(c.date || '') + '">' +
          escapeHtml(formatDate(c.date)) + '</time></div>' +
          '<h3 class="review-title">' + escapeHtml(c.title || '') + '</h3>' +
          '<p class="review-body">' + escapeHtml(c.text || '') + '</p>' +
          '<div class="review-author"><div class="avatar">' + escapeHtml(c.initials || '?') + '</div>' +
          '<div class="review-author-text"><strong>' + escapeHtml(c.name || '') + '</strong>' +
          '<span>' + escapeHtml(c.country || '') + '</span></div></div>';
        if (c.support) {
          var href = c.support.ctaHref || CONFIG.contactHref;
          var cta = c.support.ctaLabel || UI.ctaFallback;
          cards += '<div class="firm-reply" lang="' + escapeAttr(lang) + '">' +
            '<div class="firm-reply-head"><div class="avatar firm">' + escapeHtml(CONFIG.brandInitials) +
            '</div><div><strong>' + escapeHtml(CONFIG.brandName) + '</strong><span>' +
            escapeHtml(UI.supportRole) + '</span></div></div>' +
            '<p>' + escapeHtml(c.support.text || '') + '</p>' +
            '<a href="' + escapeAttr(href) + '">' + escapeHtml(cta) + '</a></div>';
        }
        cards += '</article>';
      }
    }

    var lead = UI.lead.replace(/\{topic\}/g, escapeHtml(ctx.topic));
    block.innerHTML =
      '<div class="reviews-head">' +
      '<h2>' + escapeHtml(UI.heading) + '</h2>' +
      '<p class="reviews-lead">' + lead + '</p>' +
      '</div><div class="reviews-grid" id="reviews-grid">' + cards + '</div>';

    insertNode(block, null);
  }

  function injectForm(ctx) {
    if (document.getElementById('review-comment-form')) return;
    var formLead = UI.formLead.replace(/\{topic\}/g, escapeHtml(ctx.topic));
    var privacy = UI.privacy.replace(/\{privacy\}/g, escapeAttr(CONFIG.privacyHref));

    var wrap = document.createElement('section');
    wrap.className = 'comment-form-block';
    wrap.id = 'submit-for-review';
    wrap.setAttribute('aria-labelledby', 'comment-form-heading');
    wrap.innerHTML =
      '<h2 id="comment-form-heading">' + escapeHtml(UI.formHeading) + '</h2>' +
      '<p class="comment-form-lead">' + formLead + '</p>' +
      '<form class="comment-form" id="review-comment-form" action="' + escapeAttr(CONFIG.formAction) + '" method="POST" novalidate>' +
      '<input type="hidden" name="form_type" value="comment">' +
      '<input type="hidden" name="lead_source" value="' + escapeAttr(CONFIG.leadSource) + '">' +
      '<input type="hidden" name="company" id="comment-company" value="' + escapeAttr(ctx.topic) + '">' +
      '<input type="hidden" name="slug" id="comment-slug" value="' + escapeAttr(ctx.slug) + '">' +
      '<input type="hidden" name="page_url" id="comment-page-url" value="">' +
      '<input type="hidden" name="_page" value="comment_' + escapeAttr(ctx.slug) + '">' +
      '<div class="hp" aria-hidden="true">' +
      '<label for="comment-gotcha">' + escapeHtml(UI.gotcha) + '</label>' +
      '<input type="text" id="comment-gotcha" name="_gotcha" tabindex="-1" autocomplete="off">' +
      '</div>' +
      '<div class="field-row">' +
      '<div class="field"><label for="comment-name">' + escapeHtml(UI.name) + '</label>' +
      '<input type="text" id="comment-name" name="name" required autocomplete="name" placeholder="' + escapeAttr(UI.namePh) + '"></div>' +
      '<div class="field"><label for="comment-email">' + escapeHtml(UI.email) +
      ' <span class="hint">' + escapeHtml(UI.notPublished) + '</span></label>' +
      '<input type="email" id="comment-email" name="email" required autocomplete="email" placeholder="' + escapeAttr(UI.emailPh) + '"></div>' +
      '</div>' +
      '<div class="field"><label for="comment-phone">' + escapeHtml(UI.phone) +
      ' <span class="hint">' + escapeHtml(UI.notPublished) + '</span></label>' +
      '<div class="phone-row">' +
      '<select id="comment-country-code" name="country_code" required aria-label="' + escapeAttr(UI.countryCode) + '">' +
      '<option value="" selected disabled>' + escapeHtml(UI.countryCode) + '</option>' +
      '<option value="+44">+44 UK</option><option value="+1">+1 US/CA</option>' +
      '<option value="+61">+61 AU</option><option value="+49">+49 DE</option>' +
      '<option value="+34">+34 ES</option><option value="+39">+39 IT</option>' +
      '<option value="+33">+33 FR</option><option value="+31">+31 NL</option>' +
      '</select>' +
      '<input type="tel" id="comment-phone" name="phone" required autocomplete="tel-national" placeholder="' + escapeAttr(UI.phonePh) + '">' +
      '</div></div>' +
      '<div class="field"><label for="comment-subject">' + escapeHtml(UI.subject) + '</label>' +
      '<input type="text" id="comment-subject" name="subject" required maxlength="160" placeholder="' + escapeAttr(UI.subjectPh) + '"></div>' +
      '<div class="field"><label for="comment-body">' + escapeHtml(UI.comment) + '</label>' +
      '<textarea id="comment-body" name="comment" required maxlength="4000" placeholder="' + escapeAttr(UI.bodyPh) + '"></textarea></div>' +
      '<div class="form-actions"><p class="privacy-note">' + privacy + '</p>' +
      '<button type="submit" class="btn-primary" id="comment-submit">' + escapeHtml(UI.submit) + '</button></div>' +
      '<p class="comment-form-status" id="comment-form-status" role="status" aria-live="polite"></p>' +
      '</form>';

    insertNode(wrap, document.getElementById('public-comments'));

    var form = document.getElementById('review-comment-form');
    var urlEl = document.getElementById('comment-page-url');
    if (urlEl) urlEl.value = window.location.href;
    if (!form) return;

    var status = document.getElementById('comment-form-status');
    var btn = document.getElementById('comment-submit');
    var companyEl = document.getElementById('comment-company');
    var slugEl = document.getElementById('comment-slug');
    var companyName = companyEl ? companyEl.value : '';
    var companySlug = slugEl ? slugEl.value : '';

    form.addEventListener('submit', function (e) {
      e.preventDefault();
      if (status) { status.textContent = ''; status.className = 'comment-form-status'; }
      if (!form.checkValidity()) { form.reportValidity(); return; }
      if (btn) btn.disabled = true;
      if (status) status.textContent = UI.sending;
      fetch(form.action, { method: 'POST', headers: { Accept: 'application/json' }, body: new FormData(form) })
        .then(function (res) {
          return res.json().then(function (data) {
            return { ok: res.ok, data: data };
          }).catch(function () { return { ok: res.ok, data: {} }; });
        })
        .then(function (result) {
          var data = result.data || {};
          if (result.ok && (data.code === 200 || data.status === 'success' || !data.code)) {
            if (status) { status.className = 'comment-form-status ok'; status.textContent = UI.thanks; }
            form.reset();
            if (form.elements.form_type) form.elements.form_type.value = 'comment';
            if (form.elements.lead_source) form.elements.lead_source.value = CONFIG.leadSource;
            if (companyEl) companyEl.value = companyName;
            if (slugEl) slugEl.value = companySlug;
            if (urlEl) urlEl.value = window.location.href;
          } else if (status) {
            status.className = 'comment-form-status err';
            status.textContent = (data && data.message) || UI.errSubmit;
          }
        })
        .catch(function () {
          if (status) { status.className = 'comment-form-status err'; status.textContent = UI.errNetwork; }
        })
        .finally(function () { if (btn) btn.disabled = false; });
    });
  }

  function boot() {
    var ctx = getContext();
    if (!ctx) return;

    function go() {
      injectPublished(ctx);
      injectForm(ctx);
    }

    if (window[CONFIG.commentsGlobal]) { go(); return; }
    if (!CONFIG.commentsScriptSrc) { go(); return; }
    var s = document.createElement('script');
    s.src = CONFIG.commentsScriptSrc;
    s.onload = go;
    s.onerror = go;
    document.head.appendChild(s);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', boot);
  } else {
    boot();
  }
})();
