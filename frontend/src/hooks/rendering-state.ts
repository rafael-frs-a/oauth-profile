import { useState, useEffect } from "react";

export enum RenderingState {
  IDLE = "idle",
  READY = "ready",
  RESOLVED = "resolved",
}

interface RenderingStateHook {
  state: RenderingState;
}

export default function useRenderingState(): RenderingStateHook {
  const [state, setState] = useState<RenderingState>(RenderingState.IDLE);

  useEffect(() => {
    switch (state) {
      case RenderingState.IDLE:
        setState(RenderingState.READY);
        break;
      case RenderingState.READY:
        setState(RenderingState.RESOLVED);
        break;
    }
  }, [state]);

  return { state };
}
