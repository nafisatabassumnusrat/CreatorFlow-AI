/**
 * CreatorFlow AI - Client API Service
 * Handles communication with FastAPI backend endpoints.
 */

const API_BASE = "";

const API = {
  async getMetrics() {
    const res = await fetch(`${API_BASE}/api/metrics`);
    if (!res.ok) throw new Error("Failed to load metrics");
    return await res.json();
  },

  async getVideos() {
    const res = await fetch(`${API_BASE}/api/videos`);
    if (!res.ok) throw new Error("Failed to load video projects");
    return await res.json();
  },

  async getVideo(projectId) {
    const res = await fetch(`${API_BASE}/api/videos/${projectId}`);
    if (!res.ok) throw new Error(`Project ${projectId} not found`);
    return await res.json();
  },

  async createVideo(data) {
    const res = await fetch(`${API_BASE}/api/videos/create`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    });
    if (!res.ok) throw new Error("Failed to create video project");
    return await res.json();
  },

  async createDemo() {
    const res = await fetch(`${API_BASE}/api/videos/demo`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
    });
    if (!res.ok) throw new Error("Failed to seed demo project");
    return await res.json();
  },

  async deleteVideo(projectId) {
    const res = await fetch(`${API_BASE}/api/videos/${projectId}`, {
      method: "DELETE",
    });
    if (!res.ok) throw new Error("Failed to delete video");
    return await res.json();
  },

  async triggerStage(projectId, stageName) {
    const res = await fetch(`${API_BASE}/api/videos/${projectId}/${stageName}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
    });
    if (!res.ok) throw new Error(`Failed to trigger stage: ${stageName}`);
    return await res.json();
  },

  async replan(projectId) {
    const res = await fetch(`${API_BASE}/api/videos/${projectId}/replan`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
    });
    if (!res.ok) throw new Error("Failed to replan project");
    return await res.json();
  },

  async submitApproval(projectId, approvalType, decision, edits = null) {
    const res = await fetch(`${API_BASE}/api/videos/${projectId}/approve`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        approval_type: approvalType,
        decision: decision,
        edits: edits,
      }),
    });
    if (!res.ok) throw new Error("Failed to submit approval");
    return await res.json();
  },

  async selectThumbnail(projectId, thumbnailId) {
    const res = await fetch(`${API_BASE}/api/videos/${projectId}/select-thumbnail`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ thumbnail_id: thumbnailId }),
    });
    if (!res.ok) throw new Error("Failed to select thumbnail");
    return await res.json();
  },

  async runAutonomous(projectId) {
    const res = await fetch(`${API_BASE}/api/videos/${projectId}/run-autonomous`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
    });
    if (!res.ok) throw new Error("Autonomous pipeline execution failed");
    return await res.json();
  },
};

window.API = API;
