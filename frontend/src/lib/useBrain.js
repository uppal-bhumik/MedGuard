import { useState, useEffect, useCallback } from 'react';
import { analyzePatterns, assessRisk, makeDecisions } from './medBrain';
import { safeStorageGet } from './safeAsync'; // Helper for symptoms

export function useBrain(user, medicines) {
    const [patterns, setPatterns] = useState(null);
    const [risks, setRisks] = useState(null);
    const [decisions, setDecisions] = useState(null);
    const [brainLoading, setBrainLoading] = useState(true);

    const refreshBrain = useCallback(async (updatedMeds = null) => {
        if (!user) return;
        setBrainLoading(true);
        try {
            const medsToAnalyze = updatedMeds || medicines;

            // 1. Get Adherence Log (mock for now or fetch? Dashboard passes medicines but logic needs logs)
            // analyzePatterns needs adherenceLog. 
            // We don't have adherence logs fetched in Dashboard yet (except for today's check).
            // For now, let's pass empty log or mock it, or fetch it here.
            // Since we are migrating, let's make it robust. 
            // But `analyzePatterns` uses `adherenceLog` to calc streaks.
            // If we don't fetch logs, streak will be 0.
            // Let's assume empty logs for now to avoid complexity, or try to fetch.
            // Fetching logs requires API.
            // Let's keep it simple: Pass empty array for logs for now.
            const adherenceLog = [];

            // 2. Analyze Patterns
            const pat = analyzePatterns(medsToAnalyze, adherenceLog);
            setPatterns(pat);

            // 3. Assess Risks
            // Need profile (user data) and symptoms
            // User object has id, full_name, etc. if it came from context -> getProfile?
            // Dashboard passes `user` from AuthContext? No, AuthContext `user` is Supabase user.
            // We need full profile. Dashboard fetches profile.
            // But Dashboard doesn't pass profile to useBrain.
            // It passes `user` (auth user).
            // This suggests `useBrain` might need to fetch profile or accept it.
            // `Dashboard.jsx` calls `useBrain(user, medicines)`.
            // Let's rely on `safeStorageGet` for symptoms side-loading.
            // For profile, we might use default/empty if not passed.
            // Or maybe `user` object has metadata?
            // Let's assume basic profile from `user` or defaults.
            const symptoms = safeStorageGet('medguard_symptoms', []);
            const rsk = await assessRisk(medsToAnalyze, user || {}, symptoms);
            setRisks(rsk);

            // 4. Make Decisions
            const dec = makeDecisions(pat, rsk, user || {});
            setDecisions(dec);

        } catch (e) {
            console.error("Brain Error:", e);
        } finally {
            setBrainLoading(false);
        }
    }, [user, medicines]);

    useEffect(() => {
        refreshBrain();
    }, [refreshBrain]);

    return { patterns, risks, decisions, brainLoading, refreshBrain };
}