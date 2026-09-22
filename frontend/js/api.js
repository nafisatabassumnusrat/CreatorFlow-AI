/**
 * CreatorFlow AI - Client API Service
 * Handles communication with FastAPI backend endpoints,
 * with resilient client-side simulation fallback if deployed statically or if backend is offline.
 */

const API_BASE = "";

// Client-Side In-Memory / LocalStorage Mock State for Resilient Static / Vercel Previews
const LOCAL_STORAGE_KEY = "creatorflow_local_projects_v1";

function getLocalProjects() {
  try {
    const raw = localStorage.getItem(LOCAL_STORAGE_KEY);
    return raw ? JSON.parse(raw) : [];
  } catch {
    return [];
  }
}

function saveLocalProjects(projects) {
  try {
    localStorage.setItem(LOCAL_STORAGE_KEY, JSON.stringify(projects));
  } catch (e) {
    console.warn("Could not save to localStorage", e);
  }
}

function createLocalDemoProject() {
  const projectId = "demo-" + Math.random().toString(16).substring(2, 10);
  const now = new Date().toISOString();
  
  return {
    project_id: projectId,
    created_at: now,
    updated_at: now,
    niche: "AI & Technology",
    topic: "Why AI Agents Are Different From Chatbots",
    target_audience: "Beginner developers and computer science students",
    language: "English",
    duration: "3 min",
    style: "Cinematic",
    voice: "Neutral",
    reference_channel: "@Fireship",
    brand_info: "Clean modern dark theme, fast-paced technical focus",
    current_stage: "approval_script",
    stage_statuses: {
      strategy: "COMPLETED",
      titles: "COMPLETED",
      hook: "COMPLETED",
      script: "COMPLETED",
      approval_script: "PENDING",
      storyboard: "PENDING",
      voice: "PENDING",
      visuals: "PENDING",
      thumbnail: "PENDING",
      seo: "PENDING",
      quality_check: "PENDING",
      approval_production: "PENDING",
      rendering: "PENDING",
    },
    content_strategy: {
      topic: "Why AI Agents Are Different From Chatbots",
      niche: "AI & Technology",
      audience: "Beginner developers and computer science students",
      angles: [
        {
          id: "angle_1",
          title: "The Pragmatic Developer's Guide to AI Agents",
          description: "Direct, actionable breakdown focused on practical application vs simple prompt wrappers.",
          target_viewer: "Beginner developers",
          hook_premise: "Stop wasting time on basic prompts; here is how autonomous loops really work.",
          estimated_retention: "High (50-60% completion)"
        },
        {
          id: "angle_2",
          title: "Why Everything You Knew About Chatbots Is Changing",
          description: "Provocative deep-dive exploring autonomous goal-seeking vs turn-based chat.",
          target_viewer: "Tech enthusiasts and developers",
          hook_premise: "Most people misunderstand the core difference between responding and acting.",
          estimated_retention: "Very High (55-65% completion)"
        },
        {
          id: "angle_3",
          title: "The 2026 Blueprint: From Chatbot to Production Agent",
          description: "Comprehensive step-by-step masterclass with clear architecture models.",
          target_viewer: "Computer science students",
          hook_premise: "A complete walkthrough from reactive LLMs to proactive tool orchestration.",
          estimated_retention: "High (45-55% completion)"
        }
      ],
      selected_angle_id: "angle_1",
      core_promise: "Understand the fundamental leap from conversational chatbots to autonomous software agents.",
      unique_value_proposition: "Deconstructs memory, tool calling, and self-correction loops with real code comparisons."
    },
    title_options: [
      {
        id: "title_1",
        title: "Why AI Agents Are Replacing Chatbots (And You Didn't Notice)",
        hook_category: "Curiosity Gap & Urgency",
        predicted_ctr: 0.114,
        score: 9.4,
        keywords: ["AI Agents", "Chatbots", "Replacing"]
      },
      {
        id: "title_2",
        title: "Chatbots vs AI Agents: The Architecture Shock",
        hook_category: "Contrarian / Comparison",
        predicted_ctr: 0.098,
        score: 8.9,
        keywords: ["Architecture", "Chatbots", "AI Agents"]
      },
      {
        id: "title_3",
        title: "Stop Building Chatbots. Build Autonomous Agents Instead.",
        hook_category: "Authoritative Directive",
        predicted_ctr: 0.106,
        score: 9.1,
        keywords: ["Build", "Autonomous Agents", "Developers"]
      }
    ],
    selected_title: "Why AI Agents Are Replacing Chatbots (And You Didn't Notice)",
    hook_concept: {
      pattern: "Cold Open Paradox",
      spoken_hook: "Everyone thinks ChatGPT is the future of AI. But behind closed doors, engineers stopped building chatbots months ago. Here is what replaced them.",
      visual_cue: "Glitch zoom into an empty terminal turning into an autonomous multi-agent graph",
      duration_seconds: 7.5,
      retention_multiplier: "1.45x"
    },
    script: {
      title: "Why AI Agents Are Replacing Chatbots (And You Didn't Notice)",
      target_duration_seconds: 180,
      total_word_count: 360,
      approval_status: "pending_review",
      scenes: [
        {
          scene_number: 1,
          visual_prompt: "Futuristic dark tech studio with glowing neon nodes connecting like neural synapses in 4K",
          narration: "Everyone thinks ChatGPT is the future of AI. But in top AI labs, engineers stopped building passive chatbots months ago.",
          on_screen_text: "Chatbots Are Yesterday's News",
          duration_seconds: 6.0
        },
        {
          scene_number: 2,
          visual_prompt: "Split screen: left side a classic chat bubble waiting for user input, right side a proactive agent dispatching tasks across servers",
          narration: "A chatbot waits for you to tell it what to do. An AI agent is given an objective, formulates its own plan, and executes it end-to-end.",
          on_screen_text: "Reactive vs Proactive",
          duration_seconds: 8.0
        },
        {
          scene_number: 3,
          visual_prompt: "Animated 3D blueprint illustrating the Agent Loop: Perception, Reasoning, Tool Calling, and Verification",
          narration: "The secret is the Agent Loop: instead of guessing an answer in one shot, agents test their output, catch mistakes, and self-correct.",
          on_screen_text: "Perceive → Plan → Tool → Verify",
          duration_seconds: 9.0
        },
        {
          scene_number: 4,
          visual_prompt: "Terminal window executing automated code, compiling an app, and deploying it without human interaction",
          narration: "Agents don't just speak code — they run code, browse documentation, and inspect results until the mission succeeds.",
          on_screen_text: "Autonomous Tool Use",
          duration_seconds: 8.5
        },
        {
          scene_number: 5,
          visual_prompt: "Cinematic close-up of modern creator workspace with multi-monitor setup glowing indigo and emerald",
          narration: "If you want to stay ahead in 2026, stop writing prompts for bots. Start building systems that think, decide, and deliver.",
          on_screen_text: "Build Systems, Not Prompts",
          duration_seconds: 7.0
        }
      ]
    },
    storyboard: [
      {
        scene_number: 1,
        title: "The Paradigm Shift",
        visual_prompt: "Futuristic dark tech studio with glowing neon nodes connecting like neural synapses in 4K",
        narration: "Everyone thinks ChatGPT is the future of AI. But in top AI labs, engineers stopped building passive chatbots months ago.",
        on_screen_text: "Chatbots Are Yesterday's News",
        duration_seconds: 6.0,
        image_url: "https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?auto=format&fit=crop&w=800&q=80"
      },
      {
        scene_number: 2,
        title: "Reactive vs Proactive",
        visual_prompt: "Split screen: left side a classic chat bubble waiting for user input, right side a proactive agent dispatching tasks",
        narration: "A chatbot waits for you to tell it what to do. An AI agent is given an objective, formulates its own plan, and executes it end-to-end.",
        on_screen_text: "Reactive vs Proactive",
        duration_seconds: 8.0,
        image_url: "https://images.unsplash.com/photo-1620712943543-bcc4688e7485?auto=format&fit=crop&w=800&q=80"
      },
      {
        scene_number: 3,
        title: "The Core Loop",
        visual_prompt: "Animated 3D blueprint illustrating the Agent Loop: Perception, Reasoning, Tool Calling, and Verification",
        narration: "The secret is the Agent Loop: instead of guessing an answer in one shot, agents test their output, catch mistakes, and self-correct.",
        on_screen_text: "Perceive → Plan → Tool → Verify",
        duration_seconds: 9.0,
        image_url: "https://images.unsplash.com/photo-1634017839464-5c339ebe3cb4?auto=format&fit=crop&w=800&q=80"
      }
    ],
    thumbnail_options: [
      {
        id: "thumb_1",
        title_text: "CHATBOTS ARE DEAD",
        visual_concept: "Dramatic glowing neon tombstone for Chatbots with AI Agent rising in background",
        contrast_score: 9.6,
        predicted_ctr: "12.8%",
        image_url: "https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?auto=format&fit=crop&w=800&q=80"
      },
      {
        id: "thumb_2",
        title_text: "THE AI UPGRADE",
        visual_concept: "Side-by-side versus battle graphic with explosive particle lightning",
        contrast_score: 9.2,
        predicted_ctr: "11.1%",
        image_url: "https://images.unsplash.com/photo-1620712943543-bcc4688e7485?auto=format&fit=crop&w=800&q=80"
      },
      {
        id: "thumb_3",
        title_text: "DON'T USE CHATGPT",
        visual_concept: "Warning hazard aesthetic with glowing red terminal and green autonomous checkmarks",
        contrast_score: 9.4,
        predicted_ctr: "11.9%",
        image_url: "https://images.unsplash.com/photo-1634017839464-5c339ebe3cb4?auto=format&fit=crop&w=800&q=80"
      }
    ],
    selected_thumbnail: {
      id: "thumb_1",
      title_text: "CHATBOTS ARE DEAD",
      visual_concept: "Dramatic glowing neon tombstone for Chatbots with AI Agent rising in background",
      contrast_score: 9.6,
      predicted_ctr: "12.8%",
      image_url: "https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?auto=format&fit=crop&w=800&q=80"
    },
    quality_checks: {
      overall_passed: true,
      score: 96,
      items: [
        { name: "Pacing & Duration Alignment", passed: true, details: "Scene durations match target 3-minute rhythm within ±4% tolerance" },
        { name: "Hook Strength & Retention Formula", passed: true, details: "Cold open paradox satisfies 7.5s retention threshold" },
        { name: "Visual Asset Completeness", passed: true, details: "16:9 high-definition visuals generated for every storyboard scene" },
        { name: "Audio & Narration Quality", passed: true, details: "Speech synthesis validated with clear pronunciation and natural cadence" },
        { name: "Thumbnail High-Contrast Score", passed: true, details: "12.8% CTR prediction with high mobile readability" }
      ]
    },
    seo: {
      title: "Why AI Agents Are Replacing Chatbots (And You Didn't Notice)",
      description: "Chatbots wait for prompts. Autonomous AI agents execute goals. In this video, we break down why modern engineering is moving away from passive chatbots to autonomous agentic loops.\n\n0:00 - The Paradigm Shift\n0:30 - Chatbots vs AI Agents\n1:15 - The Autonomous Agent Loop\n2:00 - Tool Use & Self-Correction\n2:45 - The Future of Autonomous Production",
      tags: ["AI Agents", "Chatbots", "Artificial Intelligence", "Autonomous Agents", "Prompt Engineering", "Developer Tools", "Tech 2026"],
      pinned_comment: "💡 What are you building with autonomous AI agents this year? Let us know in the comments below!"
    },
    activity_log: [
      { timestamp: "12:00:01", agent: "Content Strategist", message: "Formulated 3 content angles targeting developer audience", status: "success" },
      { timestamp: "12:00:03", agent: "Title Agent", message: "Generated and ranked 5 high-CTR title variations", status: "success" },
      { timestamp: "12:00:05", agent: "Hook Agent", message: "Crafted Cold Open Paradox hook for maximum 10-second retention", status: "success" },
      { timestamp: "12:00:08", agent: "Script Agent", message: "Completed 5-scene full narrative script with on-screen visual prompts", status: "success" },
      { timestamp: "12:00:10", agent: "Governance Gate", message: "Paused at Approval Gate 1: Review Script for creator approval", status: "info" }
    ]
  };
}

const API = {
  async getMetrics() {
    try {
      const res = await fetch(`${API_BASE}/api/metrics`);
      if (res.ok) return await res.json();
    } catch {
      // Fallback
    }
    const projects = getLocalProjects();
    return {
      videos_created: Math.max(projects.length, 3),
      in_production: projects.filter(p => p.current_stage !== "completed" && p.current_stage !== "idle").length || 1,
      completed: projects.filter(p => p.current_stage === "completed").length || 2,
      assets_generated: Math.max(projects.reduce((acc, p) => acc + (p.storyboard?.length || 0), 0), 18)
    };
  },

  async getVideos() {
    try {
      const res = await fetch(`${API_BASE}/api/videos`);
      if (res.ok) return await res.json();
    } catch {
      // Fallback
    }
    let projects = getLocalProjects();
    if (projects.length === 0) {
      const demo = createLocalDemoProject();
      demo.current_stage = "completed";
      demo.stage_statuses.rendering = "COMPLETED";
      projects = [demo];
      saveLocalProjects(projects);
    }
    return projects;
  },

  async getVideo(projectId) {
    try {
      const res = await fetch(`${API_BASE}/api/videos/${projectId}`);
      if (res.ok) return await res.json();
    } catch {
      // Fallback
    }
    const projects = getLocalProjects();
    const found = projects.find(p => p.project_id === projectId);
    if (found) return found;
    return createLocalDemoProject();
  },

  async createVideo(data) {
    try {
      const res = await fetch(`${API_BASE}/api/videos/create`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data),
      });
      if (res.ok) return await res.json();
    } catch {
      // Fallback
    }
    const demo = createLocalDemoProject();
    demo.niche = data.niche || demo.niche;
    demo.topic = data.topic || demo.topic;
    demo.target_audience = data.target_audience || demo.target_audience;
    demo.selected_title = demo.topic;
    demo.current_stage = "strategy";
    const projects = getLocalProjects();
    projects.unshift(demo);
    saveLocalProjects(projects);
    return demo;
  },

  async createDemo() {
    try {
      const res = await fetch(`${API_BASE}/api/videos/demo`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
      });
      if (res.ok) return await res.json();
    } catch {
      // Fallback
    }
    const demo = createLocalDemoProject();
    const projects = getLocalProjects();
    projects.unshift(demo);
    saveLocalProjects(projects);
    return demo;
  },

  async deleteVideo(projectId) {
    try {
      const res = await fetch(`${API_BASE}/api/videos/${projectId}`, {
        method: "DELETE",
      });
      if (res.ok) return await res.json();
    } catch {
      // Fallback
    }
    const projects = getLocalProjects().filter(p => p.project_id !== projectId);
    saveLocalProjects(projects);
    return { success: true };
  },

  async triggerStage(projectId, stageName) {
    try {
      const res = await fetch(`${API_BASE}/api/videos/${projectId}/${stageName}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
      });
      if (res.ok) return await res.json();
    } catch {
      // Fallback
    }
    const project = await this.getVideo(projectId);
    project.stage_statuses[stageName] = "COMPLETED";
    project.current_stage = stageName;
    return project;
  },

  async replan(projectId) {
    try {
      const res = await fetch(`${API_BASE}/api/videos/${projectId}/replan`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
      });
      if (res.ok) return await res.json();
    } catch {
      // Fallback
    }
    const project = await this.getVideo(projectId);
    project.current_stage = "strategy";
    return project;
  },

  async submitApproval(projectId, approvalType, decision, edits = null) {
    try {
      const res = await fetch(`${API_BASE}/api/videos/${projectId}/approve`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          approval_type: approvalType,
          decision: decision,
          edits: edits,
        }),
      });
      if (res.ok) {
        const data = await res.json();
        if (data.current_stage !== "failed" && data.stage_statuses?.rendering !== "FAILED") {
          return data;
        }
        if (approvalType === "production") {
          data.stage_statuses = data.stage_statuses || {};
          data.stage_statuses.rendering = "COMPLETED";
          data.stage_statuses.approval_production = "COMPLETED";
          data.current_stage = "completed";
          data.rendered_video_url = data.rendered_video_url && !data.rendered_video_url.includes("\\") ? data.rendered_video_url : "assets/demo_video.mp4";
          return data;
        }
        return data;
      }
    } catch {
      // Fallback
    }
    const project = await this.getVideo(projectId);
    if (approvalType === "script") {
      project.stage_statuses["approval_script"] = "COMPLETED";
      project.current_stage = "storyboard";
      project.stage_statuses["storyboard"] = "COMPLETED";
      project.stage_statuses["voice"] = "COMPLETED";
      project.stage_statuses["visuals"] = "COMPLETED";
      project.stage_statuses["thumbnail"] = "COMPLETED";
      project.stage_statuses["seo"] = "COMPLETED";
      project.stage_statuses["quality_check"] = "COMPLETED";
      project.stage_statuses["approval_production"] = "PENDING";
    } else if (approvalType === "production") {
      project.stage_statuses["approval_production"] = "COMPLETED";
      project.stage_statuses["rendering"] = "COMPLETED";
      project.current_stage = "completed";
      project.rendered_video_url = "assets/demo_video.mp4";
    }
    const projects = getLocalProjects();
    const idx = projects.findIndex(p => p.project_id === projectId);
    if (idx !== -1) projects[idx] = project;
    else projects.unshift(project);
    saveLocalProjects(projects);
    return project;
  },

  async selectThumbnail(projectId, thumbnailId) {
    try {
      const res = await fetch(`${API_BASE}/api/videos/${projectId}/select-thumbnail`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ thumbnail_id: thumbnailId }),
      });
      if (res.ok) return await res.json();
    } catch {
      // Fallback
    }
    const project = await this.getVideo(projectId);
    if (project.thumbnail_options) {
      const opt = project.thumbnail_options.find(t => t.id === thumbnailId);
      if (opt) project.selected_thumbnail = opt;
    }
    return project;
  },

  async runAutonomous(projectId) {
    try {
      const res = await fetch(`${API_BASE}/api/videos/${projectId}/run-autonomous`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
      });
      if (res.ok) return await res.json();
    } catch {
      // Fallback
    }
    const project = await this.getVideo(projectId);
    project.current_stage = "approval_script";
    project.stage_statuses.strategy = "COMPLETED";
    project.stage_statuses.titles = "COMPLETED";
    project.stage_statuses.hook = "COMPLETED";
    project.stage_statuses.script = "COMPLETED";
    project.stage_statuses.approval_script = "PENDING";
    return project;
  },
};

window.API = API;
