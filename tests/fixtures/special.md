---
title: Special heading fixture
permalink: /fixtures/special.html
toc: true
---

<script>
// A heading outside the article must not be included in its TOC.
document.querySelector('.site-title').insertAdjacentHTML('beforeend', '<h3 id="outside-heading">Outside heading</h3>');
</script>

## Text &lt;literal&gt; and "quotes"

A heading label must be text, not interpreted as HTML.
