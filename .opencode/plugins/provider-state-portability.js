/**
 * Keep durable OpenCode sessions portable across provider-caller rotations.
 *
 * RDC sets a one-shot historical cutoff only after the provider explicitly
 * rejects persisted reasoning state as belonging to another caller. The
 * stored transcript remains immutable; this hook edits only the in-memory
 * message copy that is about to be lowered into a provider request.
 */
export const ProviderStatePortability = async () => ({
  "experimental.chat.messages.transform": async (_input, output) => {
    const sessionID = process.env.OPENCODE_RDC_PROVIDER_STATE_SESSION_ID;
    const cutoff = Number(process.env.OPENCODE_RDC_PROVIDER_STATE_CUTOFF_MS);
    if (!sessionID || !Number.isFinite(cutoff) || cutoff <= 0) return;

    for (const message of output.messages ?? []) {
      for (const part of message.parts ?? []) {
        if (part?.type !== "reasoning" || part.sessionID !== sessionID) continue;
        const started = Number(part.time?.start ?? 0);
        if (!Number.isFinite(started) || started <= 0 || started > cutoff) continue;
        const metadata = part.metadata;
        if (!metadata || typeof metadata !== "object") continue;
        const openai = metadata.openai;
        if (!openai || typeof openai !== "object" || Array.isArray(openai)) continue;

        const cleaned = { ...openai };
        delete cleaned.itemId;
        delete cleaned.reasoningEncryptedContent;
        if (Object.keys(cleaned).length > 0) metadata.openai = cleaned;
        else delete metadata.openai;
      }
    }
  },
});
