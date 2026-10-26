/**
 * CreatorFlow AI - Main Frontend Application Logic
 */

document.addEventListener("DOMContentLoaded", () => {
  // Global State
  const state = {
    currentProject: null,
    projects: [],
    metrics: null,
    activeTab: "strategyTab",
    pollInterval: null,
  };

  // Pipeline Stage Definitions (The 12 Agent Stages)
  const STAGES = [
    { key: "strategy", label: "Strategy", icon: "💡", tab: "strategyTab" },
    { key: "titles", label: "Titles", icon: "🎯", tab: "strategyTab" },
    { key: "hook", label: "Hook", icon: "⚡", tab: "strategyTab" },
    { key: "script", label: "Script", icon: "📝", tab: "scriptTab" },
    { key: "approval_script", label: "Review Script", icon: "👤", tab: "scriptTab", isGate: true },
    { key: "storyboard", label: "Storyboard", icon: "🎬", tab: "storyboardTab" },
    { key: "voice", label: "Voiceover", icon: "🎙️", tab: "storyboardTab" },
    { key: "visuals", label: "Visuals", icon: "🎨", tab: "assetsTab" },
    { key: "thumbnail", label: "Thumbnail", icon: "🖼️", tab: "thumbnailsTab" },
    { key: "seo", label: "SEO", icon: "🔍", tab: "finalPackageTab" },
    { key: "quality_check", label: "Quality Check", icon: "🛡️", tab: "qcTab" },
    { key: "approval_production", label: "Approve Render", icon: "👤", tab: "finalPackageTab", isGate: true },
    { key: "rendering", label: "Assembly", icon: "⚙️", tab: "finalPackageTab" },
  ];

  // DOM Elements
  const els = {
    // Views
    dashboardView: document.getElementById("dashboardView"),
    workspaceView: document.getElementById("workspaceView"),
    brandHomeBtn: document.getElementById("brandHomeBtn"),
    backToDashboardBtn: document.getElementById("backToDashboardBtn"),

    // Theme
    themeToggleBtn: document.getElementById("themeToggleBtn"),

    // Modals
    openCreateModalBtn: document.getElementById("openCreateModalBtn"),
    heroCreateBtn: document.getElementById("heroCreateBtn"),
    tryDemoBtn: document.getElementById("tryDemoBtn"),
    createModal: document.getElementById("createModal"),
    closeCreateModalBtn: document.getElementById("closeCreateModalBtn"),
    cancelCreateBtn: document.getElementById("cancelCreateBtn"),
    createVideoForm: document.getElementById("createVideoForm"),
    scriptEditModal: document.getElementById("scriptEditModal"),
    closeScriptEditModalBtn: document.getElementById("closeScriptEditModalBtn"),
    cancelScriptEditBtn: document.getElementById("cancelScriptEditBtn"),
    saveScriptEditBtn: document.getElementById("saveScriptEditBtn"),
    editScriptTitle: document.getElementById("editScriptTitle"),
    editScriptNarration: document.getElementById("editScriptNarration"),

    // Activity Log Drawer
    toggleActivityLogBtn: document.getElementById("toggleActivityLogBtn"),
    closeActivityLogBtn: document.getElementById("closeActivityLogBtn"),
    activityLogDrawer: document.getElementById("activityLogDrawer"),
    activityLogList: document.getElementById("activityLogList"),
    logBadgeCount: document.getElementById("logBadgeCount"),

    // Dashboard
    metricCreated: document.getElementById("metricCreated"),
    metricInProd: document.getElementById("metricInProd"),
    metricCompleted: document.getElementById("metricCompleted"),
    metricAssets: document.getElementById("metricAssets"),
    projectsList: document.getElementById("projectsList"),
    refreshProjectsBtn: document.getElementById("refreshProjectsBtn"),

    // Workspace
    wsNichePill: document.getElementById("wsNichePill"),
    wsTopicHeading: document.getElementById("wsTopicHeading"),
    runAutonomousBtn: document.getElementById("runAutonomousBtn"),
    replanBtn: document.getElementById("replanBtn"),
    overallPipelineBadge: document.getElementById("overallPipelineBadge"),
    stagesTrack: document.getElementById("stagesTrack"),
    approvalBanner: document.getElementById("approvalBanner"),
    approvalBannerTitle: document.getElementById("approvalBannerTitle"),
    approvalBannerDesc: document.getElementById("approvalBannerDesc"),
    approvalBannerActions: document.getElementById("approvalBannerActions"),

    // Tabs
    tabButtons: document.querySelectorAll(".tab-btn"),
    tabPanes: document.querySelectorAll(".tab-pane"),

    // Strategy & Titles
    anglesContainer: document.getElementById("anglesContainer"),
    titlesContainer: document.getElementById("titlesContainer"),
    corePromiseText: document.getElementById("corePromiseText"),
    uspText: document.getElementById("uspText"),
    hookPreviewText: document.getElementById("hookPreviewText"),

    // Script
    scriptSelectedTitle: document.getElementById("scriptSelectedTitle"),
    scriptHookText: document.getElementById("scriptHookText"),
    scriptWordCount: document.getElementById("scriptWordCount"),
    scriptTargetDur: document.getElementById("scriptTargetDur"),
    scriptApprovalStatus: document.getElementById("scriptApprovalStatus"),
    scriptScenesContainer: document.getElementById("scriptScenesContainer"),
    editScriptBtn: document.getElementById("editScriptBtn"),
    regenScriptBtn: document.getElementById("regenScriptBtn"),
    approveScriptBtn: document.getElementById("approveScriptBtn"),

    // Storyboard
    storyboardSceneCount: document.getElementById("storyboardSceneCount"),
    storyboardGrid: document.getElementById("storyboardGrid"),
    regenStoryboardBtn: document.getElementById("regenStoryboardBtn"),

    // Asset Library
    assetLibraryGrid: document.getElementById("assetLibraryGrid"),

    // Quality Control
    qcStatusBadge: document.getElementById("qcStatusBadge"),
    qcSummaryHeading: document.getElementById("qcSummaryHeading"),
    qcSummarySub: document.getElementById("qcSummarySub"),
    qcChecklist: document.getElementById("qcChecklist"),
    triggerQCBtn: document.getElementById("triggerQCBtn"),

    // Thumbnail Studio (Multiple Options)
    thumbnailsGrid: document.getElementById("thumbnailsGrid"),
    regenThumbnailsBtn: document.getElementById("regenThumbnailsBtn"),
    switchThumbnailsTabBtn: document.getElementById("switchThumbnailsTabBtn"),

    // Final YouTube Package
    finalVideoPlayer: document.getElementById("finalVideoPlayer"),
    videoSource: document.getElementById("videoSource"),
    videoPlaceholderNotice: document.getElementById("videoPlaceholderNotice"),
    renderNowBtn: document.getElementById("renderNowBtn"),
    downloadVideoBtn: document.getElementById("downloadVideoBtn"),
    copyMetadataBtn: document.getElementById("copyMetadataBtn"),
    finalThumbnailImg: document.getElementById("finalThumbnailImg"),
    thumbScoreBadge: document.getElementById("thumbScoreBadge"),
    finalTitleInput: document.getElementById("finalTitleInput"),
    finalDescInput: document.getElementById("finalDescInput"),
    finalTagsContainer: document.getElementById("finalTagsContainer"),
    finalPinnedInput: document.getElementById("finalPinnedInput"),

    // Toast
    toastContainer: document.getElementById("toastContainer"),
  };

  // Toast Notification System
  function showToast(message, type = "info") {
    const toast = document.createElement("div");
    toast.className = `toast toast-${type}`;
    toast.innerHTML = `<span>${message}</span>`;
    els.toastContainer.appendChild(toast);
    setTimeout(() => {
      toast.style.opacity = "0";
      toast.style.transform = "translateY(10px)";
      setTimeout(() => toast.remove(), 200);
    }, 3500);
  }

  // Theme Management
  function initTheme() {
    const saved = localStorage.getItem("creatorflow_theme") || "light";
    document.body.className = `theme-${saved}`;
  }

  els.themeToggleBtn.addEventListener("click", () => {
    const isDark = document.body.classList.contains("theme-dark");
    const nextTheme = isDark ? "light" : "dark";
    document.body.className = `theme-${nextTheme}`;
    localStorage.setItem("creatorflow_theme", nextTheme);
  });

  // Navigation
  function showView(viewId) {
    if (viewId === "dashboardView") {
      els.dashboardView.classList.add("active");
      els.workspaceView.classList.remove("active");
      loadDashboard();
    } else if (viewId === "workspaceView") {
      els.dashboardView.classList.remove("active");
      els.workspaceView.classList.add("active");
    }
  }

  els.brandHomeBtn.addEventListener("click", () => showView("dashboardView"));
  els.backToDashboardBtn.addEventListener("click", () => showView("dashboardView"));

  // Tab Navigation
  els.tabButtons.forEach((btn) => {
    btn.addEventListener("click", () => {
      const tabId = btn.getAttribute("data-tab");
      switchTab(tabId);
    });
  });

  function switchTab(tabId) {
    state.activeTab = tabId;
    els.tabButtons.forEach((b) => {
      b.classList.toggle("active", b.getAttribute("data-tab") === tabId);
    });
    els.tabPanes.forEach((p) => {
      p.classList.toggle("active", p.id === tabId);
    });
  }

  // Activity Log Drawer Toggle
  els.toggleActivityLogBtn.addEventListener("click", () => {
    els.activityLogDrawer.classList.remove("hidden");
  });
  els.closeActivityLogBtn.addEventListener("click", () => {
    els.activityLogDrawer.classList.add("hidden");
  });

  // Create Video Modal
  const openModal = () => els.createModal.classList.remove("hidden");
  const closeModal = () => els.createModal.classList.add("hidden");

  els.openCreateModalBtn.addEventListener("click", openModal);
  els.heroCreateBtn.addEventListener("click", openModal);
  els.closeCreateModalBtn.addEventListener("click", closeModal);
  els.cancelCreateBtn.addEventListener("click", closeModal);

  // Form Submit
  els.createVideoForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    const payload = {
      niche: document.getElementById("inputNiche").value.trim(),
      topic: document.getElementById("inputTopic").value.trim(),
      target_audience: document.getElementById("inputAudience").value.trim(),
      language: document.getElementById("inputLanguage").value,
      duration: document.getElementById("inputDuration").value,
      style: document.getElementById("inputStyle").value,
      voice: document.getElementById("inputVoice").value,
      reference_channel: document.getElementById("inputReference").value.trim(),
      brand_info: document.getElementById("inputBrand").value.trim(),
    };

    closeModal();
    showToast("Initializing autonomous production agent...", "info");

    try {
      const project = await window.API.createVideo(payload);
      state.currentProject = project;
      showView("workspaceView");
      renderWorkspace(project);
      // Run autonomous pipeline
      runAutonomousPipeline();
    } catch (err) {
      showToast(err.message, "danger");
    }
  });

  // Try Demo
  els.tryDemoBtn.addEventListener("click", async () => {
    showToast("Generating autonomous demo production...", "info");
    try {
      const project = await window.API.createDemo();
      state.currentProject = project;
      showView("workspaceView");
      renderWorkspace(project);
      showToast("Demo project loaded. Review the generated script and approve to continue.", "info");
    } catch (err) {
      showToast(err.message, "danger");
    }
  });

  // Refresh Dashboard
  els.refreshProjectsBtn.addEventListener("click", loadDashboard);

  async function loadDashboard() {
    try {
      const [metrics, videos] = await Promise.all([
        window.API.getMetrics(),
        window.API.getVideos(),
      ]);
      state.metrics = metrics;
      state.projects = videos;

      els.metricCreated.textContent = metrics.videos_created;
      els.metricInProd.textContent = metrics.in_production;
      els.metricCompleted.textContent = metrics.completed;
      els.metricAssets.textContent = metrics.assets_generated;

      renderProjectsList(videos);
    } catch (err) {
      console.error(err);
    }
  }

  function renderProjectsList(videos) {
    if (!videos || videos.length === 0) {
      els.projectsList.innerHTML = `
        <div class="empty-state">
          <div class="empty-icon">🎬</div>
          <h4>No video projects yet</h4>
          <p>Click "Create New Video" or "Try Demo" to experience the autonomous production agent in action.</p>
        </div>
      `;
      return;
    }

    els.projectsList.innerHTML = videos
      .map((p) => {
        const stageStatus = p.stage_statuses[p.current_stage] || p.current_stage;
        const dur = p.duration?.value || p.duration;
        const totalScenes = p.storyboard?.length || 0;
        const dateStr = new Date(p.created_at).toLocaleDateString(undefined, {
          month: "short",
          day: "numeric",
          hour: "2-digit",
          minute: "2-digit",
        });

        return `
          <div class="project-card" data-id="${p.project_id}">
            <div class="project-card-top">
              <span class="project-card-niche">${escapeHtml(p.niche)}</span>
              <span class="badge ${p.current_stage === "completed" ? "badge-emerald" : "badge-amber"}">${escapeHtml(p.current_stage.toUpperCase())}</span>
            </div>
            <div>
              <h4 class="project-card-title">${escapeHtml(p.selected_title || p.topic)}</h4>
              <p class="project-card-audience">Target: ${escapeHtml(p.target_audience)}</p>
            </div>
            <div class="project-card-footer">
              <span>⏱ ${dur} • ${totalScenes} scenes</span>
              <span>${dateStr}</span>
            </div>
          </div>
        `;
      })
      .join("");

    // Attach click listeners to cards
    document.querySelectorAll(".project-card").forEach((card) => {
      card.addEventListener("click", async () => {
        const id = card.getAttribute("data-id");
        try {
          const project = await window.API.getVideo(id);
          state.currentProject = project;
          showView("workspaceView");
          renderWorkspace(project);
        } catch (err) {
          showToast(err.message, "danger");
        }
      });
    });
  }

  // Workspace Rendering
  function renderWorkspace(p) {
    if (!p) return;
    state.currentProject = p;

    els.wsNichePill.textContent = p.niche;
    els.wsTopicHeading.textContent = p.selected_title || p.topic;
    els.overallPipelineBadge.textContent = p.current_stage.toUpperCase();

    // Render 12-Stage Visual Pipeline Stepper
    renderPipelineStepper(p);

    // Render Human-in-the-Loop Urgent Banner
    renderApprovalBanner(p);

    // Render Tabs Content
    renderStrategyAndTitles(p);
    renderScript(p);
    renderStoryboard(p);
    renderAssetLibrary(p);
    renderThumbnailStudio(p);
    renderQualityControl(p);
    renderFinalPackage(p);

    // Render Safe Activity Log
    renderActivityLog(p);
  }

  // 12-Stage Stepper
  function renderPipelineStepper(p) {
    els.stagesTrack.innerHTML = STAGES.map((stg) => {
      const status = p.stage_statuses[stg.key] || "PENDING";
      let statusClass = "";
      if (status === "COMPLETED") statusClass = "completed";
      else if (status === "RUNNING") statusClass = "running";
      else if (status === "WAITING FOR APPROVAL") statusClass = "waiting";

      return `
        <div class="stage-step ${statusClass}" data-tab="${stg.tab}">
          <span class="stage-step-icon">${stg.icon}</span>
          <span class="stage-step-name">${stg.label}</span>
          <span class="stage-step-status">${status}</span>
        </div>
      `;
    }).join("");

    // Clicking a stage jumps to that tab
    document.querySelectorAll(".stage-step").forEach((step) => {
      step.addEventListener("click", () => {
        const tab = step.getAttribute("data-tab");
        if (tab) switchTab(tab);
      });
    });
  }

  // Human Review Gate Banner
  function renderApprovalBanner(p) {
    if (p.current_stage === "failed" || p.stage_statuses?.rendering === "FAILED") {
      els.approvalBanner.classList.remove("hidden");
      els.approvalBannerTitle.textContent = "Autonomous Assembly Recovery Required";
      els.approvalBannerDesc.textContent = p.error_message || "Video rendering encountered an error during FFmpeg compositing. Click below to retry video assembly.";
      els.approvalBannerActions.innerHTML = `
        <button id="bannerRetryRenderBtn" class="btn btn-primary btn-sm">Retry Video Assembly</button>
        <button id="bannerReplanBtn" class="btn btn-outline btn-sm">Replan Strategy</button>
      `;
      document.getElementById("bannerRetryRenderBtn")?.addEventListener("click", () => approveRenderAction());
      document.getElementById("bannerReplanBtn")?.addEventListener("click", () => {
        if (state.currentProject) {
          window.API.replan(state.currentProject.project_id).then(renderWorkspace);
        }
      });
      return;
    }

    const isScriptGate = p.waiting_for_approval_type === "script" || 
      p.stage_statuses?.approval_script === "WAITING FOR APPROVAL" || 
      (p.current_stage === "approval_script" && !p.script_approved);

    const isProductionGate = p.waiting_for_approval_type === "production" || 
      p.stage_statuses?.approval_production === "WAITING FOR APPROVAL" ||
      (p.stage_statuses?.approval_production === "PENDING" && p.stage_statuses?.quality_check === "COMPLETED" && !p.production_approved && p.current_stage !== "completed");

    if (isScriptGate) {
      els.approvalBanner.classList.remove("hidden");
      els.approvalBannerTitle.textContent = "Human Review Gate: Script & Structure";
      els.approvalBannerDesc.textContent = "The agent has generated the YouTube script and paused. Review the script below before audio synthesis & rendering.";
      els.approvalBannerActions.innerHTML = `
        <button id="bannerApproveScriptBtn" class="btn btn-primary btn-sm">Approve & Continue</button>
        <button id="bannerRegenScriptBtn" class="btn btn-outline btn-sm">Regenerate</button>
      `;
      document.getElementById("bannerApproveScriptBtn")?.addEventListener("click", () => approveScriptAction());
      document.getElementById("bannerRegenScriptBtn")?.addEventListener("click", () => regenScriptAction());
    } else if (isProductionGate) {
      els.approvalBanner.classList.remove("hidden");
      els.approvalBannerTitle.textContent = "Human Review Gate: Production Verification";
      els.approvalBannerDesc.textContent = "Quality inspection passed. Approve final rendering to composite video, voiceover, music, and text with FFmpeg.";
      els.approvalBannerActions.innerHTML = `
        <button id="bannerApproveRenderBtn" class="btn btn-primary btn-sm">Approve & Render Video</button>
      `;
      document.getElementById("bannerApproveRenderBtn")?.addEventListener("click", () => approveRenderAction());
    } else {
      els.approvalBanner.classList.add("hidden");
    }
  }

  // Tab 1: Strategy & Titles
  function renderStrategyAndTitles(p) {
    // Content Angles
    if (p.content_strategy && p.content_strategy.angles) {
      els.anglesContainer.innerHTML = p.content_strategy.angles
        .map((a) => {
          const isSelected = p.selected_angle && p.selected_angle.id === a.id;
          return `
            <div class="angle-card ${isSelected ? "selected" : ""}">
              <div class="angle-title">${isSelected ? "✓ " : ""}${escapeHtml(a.title)}</div>
              <p class="angle-desc">${escapeHtml(a.description)}</p>
              <div class="title-scores-row">
                <span class="score-chip">Viewer: ${escapeHtml(a.target_viewer)}</span>
                <span class="score-chip">Retention: ${escapeHtml(a.estimated_retention)}</span>
              </div>
            </div>
          `;
        })
        .join("");

      els.corePromiseText.textContent = p.content_strategy.core_promise || "Not formulated yet.";
      els.uspText.textContent = p.content_strategy.unique_selling_point || "Not formulated yet.";
    } else {
      els.anglesContainer.innerHTML = `<p class="info-text">Strategy formulation in progress...</p>`;
    }

    // Title Candidates
    if (p.title_options && p.title_options.length > 0) {
      els.titlesContainer.innerHTML = p.title_options
        .map((t) => {
          const isSelected = p.selected_title === t.title;
          return `
            <div class="title-card ${isSelected ? "selected" : ""}">
              <div class="title-text">${isSelected ? "★ " : ""}${escapeHtml(t.title)}</div>
              <div class="title-scores-row">
                <span class="score-chip">Clarity: ${t.clarity_score}/10</span>
                <span class="score-chip">Curiosity: ${t.curiosity_score}/10</span>
                <span class="score-chip">Relevance: ${t.relevance_score}/10</span>
                <span class="score-chip">Chars: ${t.length_chars}</span>
              </div>
            </div>
          `;
        })
        .join("");
    } else {
      els.titlesContainer.innerHTML = `<p class="info-text">Title generation pending...</p>`;
    }

    // Hook
    if (p.hook) {
      els.hookPreviewText.textContent = `"${p.hook.hook_text}" (${p.hook.hook_duration_sec}s)`;
    } else {
      els.hookPreviewText.textContent = "Hook generation pending...";
    }
  }

  // Tab 2: Script
  function renderScript(p) {
    if (!p.script) {
      els.scriptSelectedTitle.textContent = p.selected_title || p.topic;
      els.scriptHookText.textContent = "Script writing in progress...";
      els.scriptScenesContainer.innerHTML = `<p class="info-text">No script scenes generated yet.</p>`;
      return;
    }

    els.scriptSelectedTitle.textContent = p.script.selected_title || p.script.title || p.selected_title || p.topic;
    els.scriptHookText.textContent = `"${p.script.hook || p.hook_concept?.spoken_hook || p.hook?.hook_text || "Engaging hook"}"`;
    els.scriptWordCount.textContent = `${p.script.estimated_word_count || p.script.total_word_count || 300} words`;
    els.scriptTargetDur.textContent = `${p.script.target_duration_sec || p.script.target_duration_seconds || 180}s target`;
    els.scriptApprovalStatus.textContent = p.script_approved ? "Approved" : "Waiting for Review";

    els.scriptScenesContainer.innerHTML = (p.script.scenes || [])
      .map((sc) => {
        const sec = sc.section || `SCENE ${sc.scene_number}`;
        const dur = sc.duration_sec || sc.duration_seconds || 15;
        const trans = sc.transition || "Smooth cut";
        const vis = sc.visual_direction || sc.visual_prompt || "Cinematic visual";
        const txt = sc.on_screen_text || "";
        return `
          <div class="scene-block">
            <div class="scene-block-header">
              <span class="scene-badge">SCENE ${sc.scene_number} • [${escapeHtml(sec)}]</span>
              <span class="scene-dur">⏱ ${dur}s • Transition: ${escapeHtml(trans)}</span>
            </div>
            <p class="scene-narration">${escapeHtml(sc.narration)}</p>
            <div class="scene-visual-direction">
              <strong>Visual:</strong> ${escapeHtml(vis)}
            </div>
            ${txt ? `
            <div style="font-size:0.75rem; color:var(--primary); font-weight:700; margin-top:0.35rem;">
              On-Screen Text: "${escapeHtml(txt)}"
            </div>` : ""}
          </div>
        `;
      })
      .join("");
  }

  // Tab 3: Storyboard
  function renderStoryboard(p) {
    if (!p.storyboard || p.storyboard.length === 0) {
      els.storyboardSceneCount.textContent = "0 Production Scenes";
      els.storyboardGrid.innerHTML = `<p class="info-text">Storyboard generation pending...</p>`;
      return;
    }

    els.storyboardSceneCount.textContent = `${p.storyboard.length} Production Scenes`;
    els.storyboardGrid.innerHTML = p.storyboard
      .map((sc) => {
        const imgSrc = sc.image_url
          ? `/media/${p.project_id}/images/scene_${String(sc.scene_number).padStart(2, "0")}.jpg?t=${Date.now()}`
          : "";
        const audioSrc = sc.audio_url
          ? `/media/${p.project_id}/audio/scene_${String(sc.scene_number).padStart(2, "0")}.mp3?t=${Date.now()}`
          : "";

        const statusClass = (sc.asset_status || "placeholder").toLowerCase();

        return `
          <div class="storyboard-card">
            <div class="storyboard-preview-box">
              ${imgSrc ? `<img src="${imgSrc}" class="storyboard-img" alt="Scene Visual">` : `<div style="color:#64748b; font-size:0.8rem;">Visual Pending</div>`}
              <span class="scene-overlay-badge">${sc.scene_id}</span>
              <span class="asset-status-badge ${statusClass}">${escapeHtml(sc.asset_status)}</span>
            </div>
            <div class="storyboard-body">
              <div class="storyboard-meta-row">
                <span class="visual-type-tag">${escapeHtml(sc.suggested_visual_type)}</span>
                <span style="font-family:var(--font-mono); font-size:0.75rem; color:var(--text-tertiary);">⏱ ${sc.duration_sec}s</span>
              </div>
              <p class="storyboard-narration">"${escapeHtml(sc.narration)}"</p>
              <div class="storyboard-prompt-box">
                <strong>Prompt:</strong> ${escapeHtml(sc.image_prompt)}
              </div>
              ${audioSrc ? `
                <div class="storyboard-audio-row">
                  <audio controls class="mini-audio-player" src="${audioSrc}"></audio>
                </div>
              ` : ""}
            </div>
          </div>
        `;
      })
      .join("");
  }

  // Tab 4: Asset Library
  function renderAssetLibrary(p) {
    const assets = [];

    // Thumbnail
    if (p.selected_thumbnail && p.selected_thumbnail.image_url) {
      assets.push({
        type: "YouTube Thumbnail",
        name: p.selected_thumbnail.title_text,
        url: `/media/${p.project_id}/thumbnail.jpg`,
        provider: "Local Creative Engine",
        status: "GENERATED",
      });
    }

    // Storyboard Images
    if (p.storyboard) {
      p.storyboard.forEach((sc) => {
        if (sc.image_url) {
          assets.push({
            type: `Scene ${sc.scene_number} Visual`,
            name: sc.on_screen_text || `Scene ${sc.scene_number}`,
            url: `/media/${p.project_id}/images/scene_${String(sc.scene_number).padStart(2, "0")}.jpg`,
            provider: sc.provider_name || "Visual Engine",
            status: sc.asset_status,
          });
        }
      });
    }

    // Rendered Video
    if (p.rendered_video_url) {
      assets.push({
        type: "Final YouTube Video",
        name: "Full 16:9 Production Master",
        url: `/media/${p.project_id}/final_youtube_video.mp4`,
        provider: "FFmpeg Compositor",
        status: "GENERATED",
      });
    }

    if (assets.length === 0) {
      els.assetLibraryGrid.innerHTML = `<p class="info-text">No assets generated yet.</p>`;
      return;
    }

    els.assetLibraryGrid.innerHTML = assets
      .map((a) => {
        return `
          <div class="asset-item-card">
            <div class="asset-thumb-box">
              ${a.type.includes("Video") ? `<div style="color:white; font-size:1.5rem;">▶</div>` : `<img src="${a.url}" alt="${a.name}">`}
            </div>
            <div class="asset-item-info">
              <span class="asset-item-type">${a.type}</span>
              <h4 class="asset-item-name">${escapeHtml(a.name)}</h4>
              <p class="asset-item-provider">Engine: ${escapeHtml(a.provider)} • [${escapeHtml(a.status)}]</p>
            </div>
          </div>
        `;
      })
      .join("");
  }

  // Tab: Thumbnail Studio (Multiple Options)
  function renderThumbnailStudio(p) {
    if (!els.thumbnailsGrid) return;
    if (!p.thumbnail_concepts || p.thumbnail_concepts.length === 0) {
      els.thumbnailsGrid.innerHTML = `<p class="info-text">Thumbnail concepts have not been generated yet. Advance the pipeline to generate multiple options.</p>`;
      return;
    }

    els.thumbnailsGrid.innerHTML = p.thumbnail_concepts
      .map((c, idx) => {
        const isSelected = p.selected_thumbnail && p.selected_thumbnail.id === c.id;
        // Check if thumbnail option image exists
        const optImg = `/media/${p.project_id}/thumbnails/thumbnail_${c.id}.jpg?t=${Date.now()}`;
        const mainImg = `/media/${p.project_id}/thumbnail.jpg?t=${Date.now()}`;
        const imgSrc = isSelected ? mainImg : optImg;

        return `
          <div class="thumbnail-option-card ${isSelected ? 'active-selected' : ''}">
            <div class="thumbnail-option-preview">
              <img src="${imgSrc}" class="thumbnail-option-img" alt="${escapeHtml(c.title_text)}" onerror="this.src='${mainImg}'">
              <span class="thumbnail-option-badge">OPTION ${idx + 1}</span>
              <span class="thumbnail-score-badge">CTR Potential: ${c.overall_score}/10</span>
              ${isSelected ? `<span class="thumbnail-active-indicator">ACTIVE SELECTION</span>` : ""}
            </div>
            <div class="thumbnail-option-body">
              <h4 class="thumbnail-option-title">${escapeHtml(c.title_text)}</h4>
              <div class="thumbnail-scores-row">
                <span class="score-chip">Clarity: ${c.clarity_score}/10</span>
                <span class="score-chip">Curiosity: ${c.curiosity_score}/10</span>
                <span class="score-chip">Mobile: ${c.mobile_readability_score}/10</span>
                <span class="score-chip">Hierarchy: ${c.visual_hierarchy_score}/10</span>
              </div>
              <p class="thumbnail-concept-desc"><strong>Visual Concept:</strong> ${escapeHtml(c.visual_concept)}</p>
              <div class="thumbnail-details-meta">
                <span><strong>Emotion:</strong> ${escapeHtml(c.emotion)}</span> • 
                <span><strong>Colors:</strong> ${escapeHtml(c.color_direction)}</span>
              </div>
              <div class="thumbnail-action-row">
                ${isSelected
                  ? `<button class="btn btn-primary btn-sm disabled" style="width:100%;"><svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="20 6 9 17 4 12"></polyline></svg> Active Video Thumbnail</button>`
                  : `<button class="btn btn-secondary btn-sm select-thumb-btn" data-thumb-id="${c.id}" style="width:100%;"><svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg> Select This Thumbnail</button>`
                }
              </div>
            </div>
          </div>
        `;
      })
      .join("");

    // Attach click listeners to select buttons
    document.querySelectorAll(".select-thumb-btn").forEach((btn) => {
      btn.addEventListener("click", async () => {
        const thumbId = btn.getAttribute("data-thumb-id");
        try {
          showToast("Updating active YouTube thumbnail...", "info");
          const updated = await window.API.selectThumbnail(p.project_id, thumbId);
          renderWorkspace(updated);
          showToast(`Selected Thumbnail Option ${thumbId.replace("thumb_", "")}!`, "info");
        } catch (err) {
          showToast(err.message, "danger");
        }
      });
    });
  }

  // Tab 5: Quality Control
  function renderQualityControl(p) {
    if (!p.quality_checks) {
      els.qcStatusBadge.className = "qc-badge-large pending";
      els.qcStatusBadge.textContent = "PENDING";
      els.qcChecklist.innerHTML = `<p class="info-text">Quality inspection will run automatically before production rendering.</p>`;
      return;
    }

    const qc = p.quality_checks;
    els.qcStatusBadge.className = `qc-badge-large ${qc.passed ? "passed" : "failed"}`;
    els.qcStatusBadge.textContent = qc.passed ? "PASSED (100% READY)" : "FAILED (RETRY REQUIRED)";

    els.qcChecklist.innerHTML = qc.checks
      .map((chk) => {
        const icon = chk.passed ? "✅" : (chk.severity === "error" ? "❌" : "⚠️");
        return `
          <div class="check-item-row">
            <div class="check-item-left">
              <span class="check-status-icon">${icon}</span>
              <div>
                <span class="check-category">${escapeHtml(chk.category)}</span>
                <h5 class="check-name">${escapeHtml(chk.name)}</h5>
                <p class="check-details">${escapeHtml(chk.details)}</p>
              </div>
            </div>
            <span class="badge ${chk.passed ? "badge-emerald" : "badge-rose"}">${chk.passed ? "PASS" : "FLAG"}</span>
          </div>
        `;
      })
      .join("");
  }

  // Tab 6: Final YouTube Package
  function renderFinalPackage(p) {
    const isCompleted = p.stage_statuses?.rendering === "COMPLETED" || p.current_stage === "completed";
    const hasVideo = Boolean(p.rendered_video_url) || isCompleted;

    if (hasVideo) {
      els.videoPlaceholderNotice.classList.add("hidden");
      els.finalVideoPlayer.classList.remove("hidden");

      let videoUrl = p.rendered_video_url || `/media/${p.project_id}/final_youtube_video.mp4`;
      // If videoUrl is a local Windows file path, use the web-accessible media route
      if (videoUrl.startsWith("E:") || videoUrl.startsWith("C:") || videoUrl.includes("\\")) {
        videoUrl = `/media/${p.project_id}/final_youtube_video.mp4`;
      }

      els.finalVideoPlayer.onerror = () => {
        if (!els.finalVideoPlayer.src.includes("assets/demo_video.mp4")) {
          console.warn("Video stream unavailable, playing bundled preview.");
          els.finalVideoPlayer.src = "assets/demo_video.mp4";
          els.videoSource.src = "assets/demo_video.mp4";
          els.finalVideoPlayer.load();
        }
      };

      if (!els.finalVideoPlayer.src.endsWith(videoUrl)) {
        els.finalVideoPlayer.src = videoUrl;
        els.videoSource.src = videoUrl;
        els.finalVideoPlayer.load();
      }
      els.downloadVideoBtn.href = videoUrl;
      els.downloadVideoBtn.classList.remove("disabled");
    } else {
      els.videoPlaceholderNotice.classList.remove("hidden");
      els.finalVideoPlayer.classList.add("hidden");
      els.downloadVideoBtn.classList.add("disabled");
    }

    // Thumbnail Preview
    let thumbUrl = "assets/demo_thumbnail.jpg";
    if (p.selected_thumbnail && p.selected_thumbnail.image_url) {
      thumbUrl = p.selected_thumbnail.image_url;
      if (thumbUrl.startsWith("E:") || thumbUrl.startsWith("C:") || thumbUrl.includes("\\")) {
        thumbUrl = "assets/demo_thumbnail.jpg";
      }
    }
    els.finalThumbnailImg.onerror = () => {
      els.finalThumbnailImg.src = "assets/demo_thumbnail.jpg";
    };
    els.finalThumbnailImg.src = thumbUrl;
    els.thumbScoreBadge.textContent = `Score: ${p.selected_thumbnail?.overall_score || 9.6}/10`;

    // Metadata Fields
    if (p.seo) {
      els.finalTitleInput.value = p.seo.title || p.selected_title || p.topic;
      els.finalDescInput.value = p.seo.description || "";
      els.finalPinnedInput.value = p.seo.pinned_comment || "";

      els.finalTagsContainer.innerHTML = (p.seo.tags || [])
        .map((t) => `<span class="tag-pill">${escapeHtml(t)}</span>`)
        .join("");
    }
  }

  function bool(val) {
    return Boolean(val);
  }

  // Safe Activity Log Rendering
  function renderActivityLog(p) {
    if (!p.activity_logs) return;
    els.logBadgeCount.textContent = p.activity_logs.length;
    els.activityLogList.innerHTML = p.activity_logs
      .slice(-40)
      .reverse()
      .map((entry) => {
        return `
          <div class="log-entry">
            <div class="log-entry-header">
              <span class="log-stage">${escapeHtml(entry.stage)}</span>
              <span class="log-timestamp">${escapeHtml(entry.timestamp)}</span>
            </div>
            <div class="log-action">${escapeHtml(entry.action)}</div>
            ${entry.details ? `<div style="font-size:0.75rem; color:var(--text-tertiary);">${escapeHtml(entry.details)}</div>` : ""}
          </div>
        `;
      })
      .join("");
  }

  // Autonomous Execution Trigger
  async function runAutonomousPipeline() {
    if (!state.currentProject) return;
    try {
      showToast("Autonomous production pipeline started...", "info");
      const updated = await window.API.runAutonomous(state.currentProject.project_id);
      renderWorkspace(updated);
      switchTab("scriptTab");
      showToast("Script generated! Review and approve below.", "info");
    } catch (err) {
      showToast(err.message, "danger");
    }
  }

  els.runAutonomousBtn.addEventListener("click", runAutonomousPipeline);

  // Approval Handlers
  async function approveScriptAction() {
    if (!state.currentProject) return;
    try {
      showToast("Approving script and resuming pipeline...", "info");
      const updated = await window.API.submitApproval(state.currentProject.project_id, "script", "approve");
      renderWorkspace(updated);
      switchTab("storyboardTab");
      showToast("Script approved! Generated storyboards, voiceover, and visual assets.", "info");
    } catch (err) {
      showToast(err.message, "danger");
    }
  }

  async function regenScriptAction() {
    if (!state.currentProject) return;
    try {
      showToast("Regenerating script...", "info");
      const updated = await window.API.submitApproval(state.currentProject.project_id, "script", "regenerate");
      renderWorkspace(updated);
    } catch (err) {
      showToast(err.message, "danger");
    }
  }

  async function approveRenderAction() {
    if (!state.currentProject) return;
    try {
      showToast("Production approved! Commencing FFmpeg video assembly...", "info");
      const updated = await window.API.submitApproval(state.currentProject.project_id, "production", "approve");
      renderWorkspace(updated);
      switchTab("finalPackageTab");
      showToast("Video rendered successfully! YouTube package is ready.", "info");
    } catch (err) {
      showToast(err.message, "danger");
    }
  }

  // Hook up script buttons
  els.approveScriptBtn.addEventListener("click", approveScriptAction);
  els.regenScriptBtn.addEventListener("click", regenScriptAction);
  els.renderNowBtn?.addEventListener("click", approveRenderAction);

  // Edit script modal
  els.editScriptBtn.addEventListener("click", () => {
    if (!state.currentProject || !state.currentProject.script) return;
    els.editScriptTitle.value = state.currentProject.script.selected_title;
    els.editScriptNarration.value = state.currentProject.script.full_narration;
    els.scriptEditModal.classList.remove("hidden");
  });

  els.closeScriptEditModalBtn.addEventListener("click", () => els.scriptEditModal.classList.add("hidden"));
  els.cancelScriptEditBtn.addEventListener("click", () => els.scriptEditModal.classList.add("hidden"));

  els.saveScriptEditBtn.addEventListener("click", async () => {
    if (!state.currentProject) return;
    const edits = {
      selected_title: els.editScriptTitle.value.trim(),
      full_narration: els.editScriptNarration.value.trim(),
    };
    els.scriptEditModal.classList.add("hidden");
    try {
      showToast("Saving script edits...", "info");
      const updated = await window.API.submitApproval(state.currentProject.project_id, "script", "edit", edits);
      renderWorkspace(updated);
      showToast("Edits saved and pipeline resumed.", "info");
    } catch (err) {
      showToast(err.message, "danger");
    }
  });

  // Replan button
  els.replanBtn.addEventListener("click", async () => {
    if (!state.currentProject) return;
    try {
      showToast("Replanning video strategy...", "info");
      const updated = await window.API.replan(state.currentProject.project_id);
      renderWorkspace(updated);
      showToast("Project replanned.", "info");
    } catch (err) {
      showToast(err.message, "danger");
    }
  });

  // Storyboard regen
  els.regenStoryboardBtn.addEventListener("click", async () => {
    if (!state.currentProject) return;
    try {
      showToast("Regenerating storyboard scenes...", "info");
      const updated = await window.API.triggerStage(state.currentProject.project_id, "storyboard");
      renderWorkspace(updated);
    } catch (err) {
      showToast(err.message, "danger");
    }
  });

  // QC trigger
  els.triggerQCBtn.addEventListener("click", async () => {
    if (!state.currentProject) return;
    try {
      showToast("Running Quality Check...", "info");
      const updated = await window.API.triggerStage(state.currentProject.project_id, "validate");
      renderWorkspace(updated);
    } catch (err) {
      showToast(err.message, "danger");
    }
  });

  // Render Now button
  els.renderNowBtn.addEventListener("click", approveRenderAction);

  // Switch to Thumbnails Studio from Final Package Tab
  els.switchThumbnailsTabBtn?.addEventListener("click", () => {
    switchTab("thumbnailsTab");
  });

  // Regenerate Thumbnails
  els.regenThumbnailsBtn?.addEventListener("click", async () => {
    if (!state.currentProject) return;
    try {
      showToast("Generating fresh thumbnail concepts...", "info");
      const updated = await window.API.triggerStage(state.currentProject.project_id, "thumbnail");
      renderWorkspace(updated);
      showToast("New thumbnail concepts generated!", "info");
    } catch (err) {
      showToast(err.message, "danger");
    }
  });

  // Copy Buttons
  document.querySelectorAll(".copy-btn").forEach((btn) => {
    btn.addEventListener("click", () => {
      const targetId = btn.getAttribute("data-target");
      const input = document.getElementById(targetId);
      if (input) {
        navigator.clipboard.writeText(input.value);
        showToast("Copied to clipboard!", "info");
      }
    });
  });

  els.copyMetadataBtn.addEventListener("click", () => {
    if (!state.currentProject || !state.currentProject.seo) return;
    const p = state.currentProject;
    const metaText = `TITLE:\n${p.seo.title}\n\nDESCRIPTION:\n${p.seo.description}\n\nTAGS:\n${(p.seo.tags || []).join(", ")}\n\nPINNED COMMENT:\n${p.seo.pinned_comment}`;
    navigator.clipboard.writeText(metaText);
    showToast("Full YouTube metadata package copied to clipboard!", "info");
  });

  // Helpers
  function escapeHtml(str) {
    if (!str) return "";
    return String(str)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#039;");
  }

  // Initial load
  initTheme();
  loadDashboard();
});
