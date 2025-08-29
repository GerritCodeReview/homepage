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
      <h1>Gerrit Code Review</h1>
      <p>The open source, patchset based, code review platform for Git-based development</p>
      <a href="https://gerrit-releases.storage.googleapis.com/gerrit-3.12.2.war" class="btn-modern">Download Gerrit 3.12.2</a>
       <a href="#getting-started" class="btn-modern btn-outline" _target="blank">
        <i class="fas fa-rocket"></i>
        Try now
      </a>
    </div>
  </div>
</div>

<div class="wrapper">
  <p style="text-align: center; font-size: 1.3rem; margin-bottom: 4rem;">
    Gerrit is a web-based code review system that enables teams to collaborate on Git repositories with powerful patchset based review workflows, fine-grained permissions, and seamless integration with CI/CD pipelines.
  </p>

<div class="section-header">
  <div class="section-icon">🚀</div>
  <h2>Why Teams Choose Gerrit</h2>
  <div class="section-subtitle">Powerful features that make Gerrit the preferred choice for enterprise code review</div>
</div>

<div class="why-gerrit-section">
  <div class="why-gerrit-grid">
    <div class="why-gerrit-card">
      <div class="why-gerrit-icon">
        <i class="fas fa-shield-alt"></i>
      </div>
      <h3>Open Source Freedom</h3>
      <p>100% open source with no licensing fees or vendor lock-in. Use at any scale without restrictions, with full access to source code and community-driven development.</p>
    </div>
    
    <div class="why-gerrit-card">
      <div class="why-gerrit-icon">
        <i class="fas fa-users"></i>
      </div>
      <h3>Team Collaboration</h3>
      <p>Advanced review workflows with inline comments, patchset management, and configurable approval processes that scale from small teams to thousands of developers.</p>
    </div>
    
    <div class="why-gerrit-card">
      <div class="why-gerrit-icon">
        <i class="fas fa-rocket"></i>
      </div>
      <h3>Git-Native Performance</h3>
      <p>Built specifically for Git with optimized performance, sophisticated branching strategies, and seamless integration with existing Git workflows.</p>
    </div>
    
    <div class="why-gerrit-card">
      <div class="why-gerrit-icon">
        <i class="fas fa-cogs"></i>
      </div>
      <h3>Extensible Platform</h3>
      <p>Plugin architecture with 100+ community plugins and REST API for custom integrations with your existing tools and workflows.</p>
    </div>
  </div>
</div>

<div class="section-header">
  <div class="section-icon">🔍</div>
  <h2>Core Features</h2>
  <div class="section-subtitle">Everything you need for effective code review and collaboration</div>
</div>

<div class="feature__wrapper">
  <div class="feature__item">
    <div class="archive__item">
      <div class="archive__item-body">
        <h3 class="archive__item-title">Fine Grained Permission Model</h3>
        <div class="archive__item-excerpt">
          <p>Enterprise-grade access control that enables organizations to enforce strict security policies, maintain compliance requirements, and manage complex team structures with precise control over who can access what code. Perfect for regulated industries and large organizations with diverse development teams.</p>
        </div>
      </div>
    </div>
  </div>

  <div class="feature__item">
    <div class="archive__item">
      <div class="archive__item-body">
        <h3 class="archive__item-title">Git-Native Workflow</h3>
        <div class="archive__item-excerpt">
          <p>Unlike other SCMs, Gerrit's unique patch-based code review system more closely resembles the proven mailing list workflow used by Git itself and the Linux kernel, where patches are reviewed and iterated on before being applied to the main repository, ensuring higher code quality and better collaboration.</p>
        </div>
      </div>
    </div>
  </div>

  <div class="feature__item">
    <div class="archive__item">
      <div class="archive__item-body">
        <h3 class="archive__item-title">Enterprise Scalability</h3>
        <div class="archive__item-excerpt">
          <p>Get <b>out-of-hours support</b> with <b>strict SLAs</b> for your on-prem installation, ensuring your enterprise deployment has the professional support it needs. Plus, enjoy multi-node scalability with <b>no-downtime upgrades</b> for enterprise-grade reliability.</p>
        </div>
        <a href="https://www.gerritcodereview.com/support.html#enterprise-support" class="btn-modern btn-small">
          <i class="fas fa-rocket"></i>
          Enterprise Support
        </a>
      </div>
    </div>
  </div>
</div>

<div class="notice--info">
  {{ notice-text | markdownify }}
</div>

<div class="section-header">
  <div class="section-icon">🛠️</div>
  <h2>Developer Experience</h2>
  <div class="section-subtitle">Built for developers, with the tools and integrations you need to be productive</div>
</div>

<div class="dev-experience-section">
  <div class="dev-experience-grid">
    <div class="dev-experience-card">
      <div class="dev-experience-header">
        <i class="fas fa-code-branch"></i>
        <h3>Patchset-Based Workflow</h3>
      </div>
      <div class="dev-experience-content">
        <p>Unlike other SCMs, Gerrit's adopts a patch-based code review system which more closely resembles the proven mailing list workflow used by Git itself and the Linux kernel.</p>
        <ul class="feature-list">
          <li><i class="fas fa-check"></i> Patchset-based reviews</li>
          <li><i class="fas fa-check"></i> Iterative refinement</li>
          <li><i class="fas fa-check"></i> Git-native workflow</li>
          <li><i class="fas fa-check"></i> Proven collaboration model</li>
        </ul>
      </div>
    </div>
    
    <div class="dev-experience-card">
      <div class="dev-experience-header">
        <i class="fas fa-code"></i>
        <h3>REST API & Integrations</h3>
      </div>
      <div class="dev-experience-content">
        <p>Comprehensive REST API for seamless integration with your existing development tools and CI/CD pipelines.</p>
        <ul class="feature-list">
          <li><i class="fas fa-check"></i> Full REST API coverage</li>
          <li><i class="fas fa-check"></i> Webhook support</li>
          <li><i class="fas fa-check"></i> CLI tools</li>
          <li><i class="fas fa-check"></i> IDE integrations</li>
        </ul>
        <a href="https://gerrit-review.googlesource.com/Documentation/rest-api.html" class="btn-modern btn-small">
          <i class="fas fa-code"></i>
          View API Docs
        </a>
      </div>
    </div>
    
    <div class="dev-experience-card">
      <div class="dev-experience-header">
        <i class="fas fa-puzzle-piece"></i>
        <h3>Plugin Ecosystem</h3>
      </div>
      <div class="dev-experience-content">
        <p>Extend and customize Gerrit with 100+ community plugins or build your own to fit your specific workflow needs.</p>
        <ul class="feature-list">
          <li><i class="fas fa-check"></i> 100+ community plugins</li>
          <li><i class="fas fa-check"></i> Custom plugin development</li>
          <li><i class="fas fa-check"></i> Plugin marketplace</li>
          <li><i class="fas fa-check"></i> Easy installation</li>
        </ul>
        <a href="plugins.html" class="btn-modern btn-small">
          <i class="fas fa-puzzle-piece"></i>
          Browse Plugins
        </a>
      </div>
    </div>
  </div>
</div>

<div class="section-header">
  <div class="section-icon">🔄</div>
  <h2>CI/CD Integration</h2>
  <div class="section-subtitle">Seamlessly integrate with your existing CI/CD pipeline</div>
</div>

<div class="cicd-section">
  
  <div class="cicd-grid">
    <a style="cursor: default; color: black; text-decoration:none;" href="https://www.jenkins.io" target="_blank">
      <div class="cicd-card">
        <div class="cicd-icon">
          <i class="fab fa-jenkins"></i>
        </div>
        <h3>Jenkins Integration</h3>
        <p>Integrate with Jenkins pipelines for automated testing, building, and deployment workflows.</p>
        <div class="cicd-features">
          <span class="cicd-tag">Pipeline Support</span>
          <span class="cicd-tag">Build Status</span>
          <span class="cicd-tag">Auto-trigger</span>
        </div>
      </div>
    </a>
    
    <a style="cursor: default; color: black; text-decoration:none;" href="https://github.com/features/actions" target="_blank">
      <div class="cicd-card">
        <div class="cicd-icon">
          <i class="fab fa-github"></i>
        </div>
        <h3>GitHub Actions</h3>
        <p>Connect with GitHub Actions for automated testing and quality checks in your development workflow.</p>
        <div class="cicd-features">
          <span class="cicd-tag">Workflow Integration</span>
          <span class="cicd-tag">Status Checks</span>
          <span class="cicd-tag">Parallel Jobs</span>
        </div>
      </div>
    </a>
    
    <div class="cicd-card">
      <div class="cicd-icon">
        <i class="fas fa-link"></i>
      </div>
      <h3>Custom Webhooks</h3>
      <p>Webhook support for any CI/CD system, allowing you to integrate with your preferred tools and platforms.</p>
      <div class="cicd-features">
        <span class="cicd-tag">REST API</span>
        <span class="cicd-tag">Event-driven</span>
        <span class="cicd-tag">Flexible</span>
      </div>
    </div>
    
    <a style="cursor: default; color: black; text-decoration:none;" href="https://zuul-ci.org/docs/zuul/latest/index.html" target="_blank">
    <div class="cicd-card">
      <div class="cicd-icon">
        <img src="/images/zuul.ico" alt="Zuul Logo" class="zuul-logo">
      </div>
      <h3>Zuul Gating System</h3>
      <p>Advanced gating system that ensures code quality by running tests before merging, preventing broken code from entering the repository.</p>
      <div class="cicd-features">
        <span class="cicd-tag">Pre-merge Testing</span>
        <span class="cicd-tag">Gating Workflows</span>
        <span class="cicd-tag">Quality Assurance</span>
      </div>
    </div>
    </a>
  </div>
</div>

<div class="section-header">
  <div class="section-icon">📈</div>
  <h2>Trusted by Industry Leaders</h2>
  <div class="section-subtitle">Some of the biggest open source projects in the world succesfully use Gerrit for their Code Review workflows</div>
</div>

<div class="company-logos">
  <div class="logo-grid">
    <div class="logo-item">
      <div class="logo-container">
        <i class="fab fa-android"></i>
        <a href="https://android.googlesource.com/"><span class="logo-text">Android</span></a>
      </div>
    </div>
    
    <div class="logo-item">
      <div class="logo-container">
        <i class="fab fa-chrome"></i>
        <a href="https://chromium.googlesource.com/"><span class="logo-text">Chrome</span></a>
      </div>
    </div>
    
    <div class="logo-item">
      <div class="logo-container">
        <i class="fas fa-cloud"></i>
        <a href="https://review.opendev.org"><span class="logo-text">OpenInfra Foundation</span></a>
      </div>
    </div>
    
    <div class="logo-item">
      <div class="logo-container">
        <i class="fas fa-git"></i>
        <span class="logo-text">JGit</span>
      </div>
    </div>
    
    <div class="logo-item">
      <div class="logo-container">
        <i class="fas fa-cube"></i>
        <a href="https://codereview.qt-project.org"><span class="logo-text">Qt</span></a>
      </div>
    </div>
  </div>
</div>

<div class="section-header" id="getting-started">
  <div class="section-icon">🎯</div>
  <h2>Getting Started</h2>
  <div class="section-subtitle">Get up and running with Gerrit in minutes with our simple setup guides</div>
</div>

<div class="getting-started-grid">
  <div class="getting-started-card">
    <div class="card-header">
      <i class="fas fa-rocket"></i>
      <h3>Standalone</h3>
    </div>
    <div class="card-content">
      <p>Get Gerrit running locally in under 2 minutes</p>
      <div class="code-block">
        <div class="code-header">
          <span>Terminal</span>
        </div>
        <pre><code># Download the latest release
wget https://gerrit-releases.storage.googleapis.com/gerrit-3.12.2.war

# Initialize a new Gerrit site
java -jar gerrit-3.12.2.war init -d /path/to/gerrit --dev --batch --install-all-plugins

# Start Gerrit
cd /path/to/gerrit && bin/gerrit.sh start</code></pre>
      </div>
      <a href="https://gerrit-releases.storage.googleapis.com/gerrit-3.12.2.war" class="btn-modern btn-small">Download Now</a>
    </div>
  </div>

  <div class="getting-started-card">
    <div class="card-header">
      <i class="fab fa-docker"></i>
      <h3>Docker Deployment</h3>
    </div>
    <div class="card-content">
      <p>Run Gerrit in a container for easy deployment</p>
      <div class="code-block">
        <div class="code-header">
          <span>Docker</span>
        </div>
        <pre><code># Run with Docker
docker run -d \
  -p 8080:8080 \
  -p 29418:29418 \
  --name gerrit \
  gerritcodereview/gerrit:latest</code></pre>
      </div>
      <a href="https://hub.docker.com/r/gerritcodereview/gerrit" class="btn-modern btn-small">View on Docker Hub</a>
    </div>
  </div>

  <div class="getting-started-card">
    <div class="card-header">
      <i class="fas fa-cloud"></i>
      <h3>GerritHub.io</h3>
    </div>
          <div class="card-content">
        <p>Readily available Gerrit instance. GerritHub.io is free to use, even for private repositories, making it perfect for teams of any size.</p>
        <p>Seamlessly integrate your GitHub repositories, automatically replicate data from Gerrit to GitHub so to leverage Gerrit's code review capabilities while maintaining the visibility and social features of GitHub.</p>
        <a href="https://gerrithub.io" class="btn-modern btn-small">Visit GerritHub.io</a>
      </div>
  </div>
</div>

<div class="section-header">
  <div class="section-icon">🔗</div>
  <h2>Resources & Community</h2>
  <div class="section-subtitle">Everything you need to learn, connect, and get support</div>
</div>

<div class="resources-grid">
  <div class="resource-card">
    <div class="resource-icon">
      <i class="fas fa-book"></i>
    </div>
    <h3>Documentation</h3>
    <p>Complete user and admin guides to get the most out of Gerrit</p>
    <a href="https://gerrit-review.googlesource.com/Documentation/" class="resource-link">
      <span>View Documentation</span>
      <i class="fas fa-arrow-right"></i>
    </a>
  </div>

  <div class="resource-card">
    <div class="resource-icon">
      <i class="fas fa-code"></i>
    </div>
    <h3>API Reference</h3>
    <p>Comprehensive REST API documentation for integrations</p>
    <a href="https://gerrit-review.googlesource.com/Documentation/rest-api.html" class="resource-link">
      <span>View API Docs</span>
      <i class="fas fa-arrow-right"></i>
    </a>
  </div>

  <div class="resource-card">
    <div class="resource-icon">
      <i class="fas fa-envelope"></i>
    </div>
    <h3>Mailing List</h3>
    <p>Join the official Gerrit community discussion forum</p>
    <a href="https://groups.google.com/group/repo-discuss" class="resource-link">
      <span>Join Discussion</span>
      <i class="fas fa-arrow-right"></i>
    </a>
  </div>

  <div class="resource-card">
    <div class="resource-icon">
      <i class="fas fa-comments"></i>
    </div>
    <h3>Discord Server</h3>
    <p>Chat with the community in real-time on Discord</p>
    <a href="https://discord.gg/eEZQrtzAwV" class="resource-link">
      <span>Join Discord</span>
      <i class="fas fa-arrow-right"></i>
    </a>
  </div>
</div>

<div class="cta-section">
  <div class="cta-content">
    <h2>Ready to Transform Your Code Review Process?</h2>
    <p>Join thousands of teams already using the most powerful code review platform available.</p>
    <div class="cta-buttons">
      <a href="https://gerrit-releases.storage.googleapis.com/gerrit-3.12.2.war" class="btn-modern btn-large">
        <i class="fas fa-download"></i>
        Download Gerrit 3.12.2
      </a>
      <a href="https://gerrit-review.googlesource.com/Documentation/" class="btn-modern btn-outline">
        <i class="fas fa-book"></i>
        View Documentation
      </a>
    </div>
  </div>
</div>
