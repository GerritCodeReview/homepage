---
title: "Gerrit Code Review"
permalink: /
layout: default

---

<div class="hero-section">
  <div class="wrapper">
    <div class="hero-content">
      <div class="hero-icon">
        <img src="/images/gerrit-logo.svg" alt="Gerrit Logo" class="gerrit-logo">
      </div>
      <h1>{{ site.data.content.hero.title }}</h1>
      <p>{{ site.data.content.hero.subtitle }}</p>
      <a href="{{ site.data.content.links.gerrit_war }}" class="btn-modern">{{ site.data.content.hero.download_button }}</a>
       <a href="{{ site.data.content.links.getting_started }}" class="btn-modern btn-outline" _target="blank">
        <i class="{{ site.data.content.hero.try_now_icon }}"></i>
        {{ site.data.content.hero.try_now_button }}
      </a>
    </div>
  </div>
</div>

<div class="wrapper">
  <p style="text-align: center; font-size: 1.3rem; margin-bottom: 4rem;">
    {{ site.data.content.intro.text }}
  </p>

<div class="section-header">
  <div class="section-icon">🚀</div>
  <h2>{{ site.data.content.why_gerrit.title }}</h2>
  <div class="section-subtitle">{{ site.data.content.why_gerrit.subtitle }}</div>
</div>

<div class="why-gerrit-section">
  <div class="why-gerrit-grid">
    {% for card in site.data.content.why_gerrit.cards %}
    <div class="why-gerrit-card">
      <div class="why-gerrit-icon">
        <i class="{{ card.icon }}"></i>
      </div>
      <h3>{{ card.title }}</h3>
      <p>{{ card.text }}</p>
    </div>
    {% endfor %}
  </div>
</div>

<div class="section-header">
  <div class="section-icon">🔍</div>
  <h2>{{ site.data.content.core_features.title }}</h2>
  <div class="section-subtitle">{{ site.data.content.core_features.subtitle }}</div>
</div>

<div class="feature__wrapper">
  {% for feature in site.data.content.core_features.features %}
  <div class="feature__item">
    <div class="archive__item">
      <div class="archive__item-body">
        <h3 class="archive__item-title">{{ feature.title }}</h3>
        <div class="archive__item-excerpt">
          <p>{{ feature.text }}</p>
        </div>
        {% if feature.button %}
        <a href="{{ feature.button_url }}" class="btn-modern btn-small">
          <i class="{{ feature.button_icon }}"></i>
          {{ feature.button }}
        </a>
        {% endif %}
      </div>
    </div>
  </div>
  {% endfor %}
</div>

<div class="notice--info">
  {{ notice-text | markdownify }}
</div>

<div class="section-header">
  <div class="section-icon">🛠️</div>
  <h2>{{ site.data.content.dev_experience.title }}</h2>
  <div class="section-subtitle">{{ site.data.content.dev_experience.subtitle }}</div>
</div>

<div class="dev-experience-section">
  <div class="dev-experience-grid">
    {% for card in site.data.content.dev_experience.cards %}
    <div class="dev-experience-card">
      <div class="dev-experience-header">
        <i class="{{ card.icon }}"></i>
        <h3>{{ card.title }}</h3>
      </div>
      <div class="dev-experience-content">
        <p>{{ card.text }}</p>
        <ul class="feature-list">
          {% for feature in card.features %}
          <li><i class="{{ card.features_icon }}"></i> {{ feature }}</li>
          {% endfor %}
        </ul>
        {% if card.button %}
        <a href="{{ card.button_url }}" class="btn-modern btn-small">
          <i class="{{ card.button_icon }}"></i>
          {{ card.button }}
        </a>
        {% endif %}
      </div>
    </div>
    {% endfor %}
  </div>
</div>

<div class="section-header">
  <div class="section-icon">🔄</div>
  <h2>{{ site.data.content.cicd.title }}</h2>
  <div class="section-subtitle">{{ site.data.content.cicd.subtitle }}</div>
</div>

<div class="cicd-section">
  
  <div class="cicd-grid">
    {% for card in site.data.content.cicd.cards %}
    <a style="cursor: default; color: black; text-decoration:none;" href="{{ card.url }}" target="_blank">
      <div class="cicd-card">
        <div class="cicd-icon">
          {% if card.icon == 'zuul' %}
          <img src="/images/zuul.ico" alt="Zuul Logo" class="zuul-logo">
          {% else %}
          <i class="{{ card.icon }}"></i>
          {% endif %}
        </div>
        <h3>{{ card.title }}</h3>
        <p>{{ card.text }}</p>
        <div class="cicd-features">
          {% for tag in card.tags %}
          <span class="cicd-tag">{{ tag }}</span>
          {% endfor %}
        </div>
      </div>
    </a>
    {% endfor %}
  </div>
</div>

<div class="section-header">
  <div class="section-icon">📈</div>
  <h2>{{ site.data.content.trusted_by.title }}</h2>
  <div class="section-subtitle">{{ site.data.content.trusted_by.subtitle }}</div>
</div>

<div class="company-logos">
  <div class="logo-grid">
    {% for logo in site.data.content.trusted_by.logos %}
    <div class="logo-item">
      <div class="logo-container">
        <i class="{{ logo.icon }}"></i>
        <a href="{{ logo.url }}"><span class="logo-text">{{ logo.name }}</span></a>
      </div>
    </div>
    {% endfor %}
  </div>
</div>

<div class="section-header" id="getting-started">
  <div class="section-icon">🎯</div>
  <h2>{{ site.data.content.getting_started.title }}</h2>
  <div class="section-subtitle">{{ site.data.content.getting_started.subtitle }}</div>
</div>

<div class="getting-started-grid">
  {% for card in site.data.content.getting_started.cards %}
  <div class="getting-started-card">
    <div class="card-header">
      <i class="{{ card.icon }}"></i>
      <h3>{{ card.title }}</h3>
    </div>
    <div class="card-content">
      <p>{{ card.text }}</p>
      {% if card.subtext %}
      <p>{{ card.subtext }}</p>
      {% endif %}
      {% if card.code_block %}
      <div class="code-block">
        <div class="code-header">
          <span>Terminal</span>
        </div>
        <pre><code>{{ card.code_block }}</code></pre>
      </div>
      {% endif %}
      <a href="{{ card.button_url }}" class="btn-modern btn-small">{{ card.button }}</a>
    </div>
  </div>
  {% endfor %}
</div>

<div class="section-header">
  <div class="section-icon">🔗</div>
  <h2>{{ site.data.content.resources.title }}</h2>
  <div class="section-subtitle">{{ site.data.content.resources.subtitle }}</div>
</div>

<div class="resources-grid">
  {% for card in site.data.content.resources.cards %}
  <div class="resource-card">
    <div class="resource-icon">
      <i class="{{ card.icon }}"></i>
    </div>
    <h3>{{ card.title }}</h3>
    <p>{{ card.text }}</p>
    <a href="{{ card.button_url }}" class="resource-link">
      <span>{{ card.button }}</span>
      <i class="{{ card.button_icon }}"></i>
    </a>
  </div>
  {% endfor %}
</div>

<div class="cta-section">
  <div class="cta-content">
    <h2>{{ site.data.content.cta.title }}</h2>
    <p>{{ site.data.content.cta.subtitle }}</p>
    <div class="cta-buttons">
      <a href="{{ site.data.content.cta.download_button_url }}" class="btn-modern btn-large">
        <i class="{{ site.data.content.cta.download_button_icon }}"></i>
        {{ site.data.content.cta.download_button }}
      </a>
      <a href="{{ site.data.content.cta.docs_button_url }}" class="btn-modern btn-outline">
        <i class="{{ site.data.content.cta.docs_button_icon }}"></i>
        {{ site.data.content.cta.docs_button }}
      </a>
    </div>
  </div>
</div>