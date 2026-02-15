/**
 * MedGuard — API Service
 * Connects to local FastAPI backend (http://localhost:8000)
 */

const API_BASE_URL = "http://localhost:8000/api";

async function request(endpoint, options = {}) {
    const url = `${API_BASE_URL}${endpoint}`;
    const headers = {
        'Content-Type': 'application/json',
        ...options.headers,
    };

    try {
        const response = await fetch(url, { ...options, headers });

        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            throw new Error(errorData.detail || `HTTP error ${response.status}`);
        }

        return await response.json();
    } catch (error) {
        console.error(`[API] Error request ${endpoint}:`, error);
        throw error;
    }
}

export const api = {
    // ── Profile ─────────────────────────────────────────────
    getProfile: (userId) => request(`/profiles/${userId}`),

    createOrUpdateProfile: (profileData) => request(`/profile`, {
        method: 'POST',
        body: JSON.stringify(profileData),
    }),

    // ── Medicine Analysis (OCR) ─────────────────────────────
    analyzePrescription: async (file) => {
        const formData = new FormData();
        formData.append('file', file);

        const response = await fetch(`${API_BASE_URL}/prescriptions/upload`, {
            method: 'POST',
            body: formData,
        });

        if (!response.ok) {
            const error = await response.json().catch(() => ({}));
            throw new Error(error.detail || 'Analysis failed');
        }
        return await response.json();
    },

    // ── Medicines ───────────────────────────────────────────
    getMedicines: (userId) => request(`/medicines/${userId}`),

    createMedicine: (medicineData) => request(`/medicines`, {
        method: 'POST',
        body: JSON.stringify(medicineData),
    }),

    updateMedicine: (id, updates) => request(`/medicines/${id}`, {
        method: 'PATCH',
        body: JSON.stringify(updates),
    }),

    deleteMedicine: (id) => request(`/medicines/${id}`, {
        method: 'DELETE',
    }),

    // ── Adherence ───────────────────────────────────────────
    logAdherence: (logData) => request(`/adherence_log`, {
        method: 'POST',
        body: JSON.stringify(logData),
    }),
};
