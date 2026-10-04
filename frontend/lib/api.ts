import { WebsiteAnalysisData } from "@/types";

const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_BASE_URL ||
  process.env.NEXT_PUBLIC_API_URL ||
  "http://localhost:8000";

const DEFAULT_TIMEOUT_MS = 15000;

async function parseErrorMessage(response: Response, fallback: string): Promise<string> {
  if (response.status === 413) {
    return "The submitted input or image is too large. Please submit a smaller payload.";
  }
  if (response.status === 415) {
    return "Unsupported file format. Please upload a PNG, JPEG, or WEBP image.";
  }
  if (response.status === 429) {
    return "Too many requests. Please wait a moment before submitting another analysis.";
  }
  if (response.status >= 500) {
    return "RakshaScan could not complete the analysis right now. Please try again.";
  }

  try {
    const errorData = await response.json();
    if (errorData?.detail?.message) {
      return errorData.detail.message;
    }
    if (typeof errorData?.detail === "string") {
      return errorData.detail;
    }
  } catch {
    // If JSON parsing fails, fallback to provided string
  }
  return fallback;
}

export async function analyzeUrlApi(url: string): Promise<WebsiteAnalysisData> {
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), DEFAULT_TIMEOUT_MS);

  try {
    const response = await fetch(`${API_BASE_URL}/api/v1/analyze/url`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ url }),
      signal: controller.signal,
    });

    if (!response.ok) {
      const errorMsg = await parseErrorMessage(
        response,
        `Analysis request failed with status ${response.status}.`
      );
      throw new Error(errorMsg);
    }

    return await response.json();
  } catch (error: unknown) {
    if (error instanceof Error) {
      if (error.name === "AbortError") {
        throw new Error("The analysis request timed out. The server took too long to respond.");
      }
      if (
        error.message.includes("Failed to fetch") ||
        error.message.includes("NetworkError") ||
        error.message.includes("ECONNREFUSED")
      ) {
        throw new Error(
          `Cannot connect to the RakshaScan server at ${API_BASE_URL}. Please ensure the backend is running.`
        );
      }
      throw error;
    }
    throw new Error("An unexpected network error occurred while analyzing the URL.");
  } finally {
    clearTimeout(timeoutId);
  }
}

export async function analyzeMessageApi(text: string): Promise<WebsiteAnalysisData> {
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), DEFAULT_TIMEOUT_MS);

  try {
    const response = await fetch(`${API_BASE_URL}/api/v1/analyze/message`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ text }),
      signal: controller.signal,
    });

    if (!response.ok) {
      const errorMsg = await parseErrorMessage(
        response,
        `Message analysis request failed with status ${response.status}.`
      );
      throw new Error(errorMsg);
    }

    return await response.json();
  } catch (error: unknown) {
    if (error instanceof Error) {
      if (error.name === "AbortError") {
        throw new Error("The analysis request timed out. The server took too long to respond.");
      }
      if (
        error.message.includes("Failed to fetch") ||
        error.message.includes("NetworkError") ||
        error.message.includes("ECONNREFUSED")
      ) {
        throw new Error(
          `Cannot connect to the RakshaScan server at ${API_BASE_URL}. Please ensure the backend is running.`
        );
      }
      throw error;
    }
    throw new Error("An unexpected network error occurred while analyzing the message.");
  } finally {
    clearTimeout(timeoutId);
  }
}

export async function analyzeScreenshotApi(file: File): Promise<WebsiteAnalysisData> {
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), DEFAULT_TIMEOUT_MS);

  try {
    const formData = new FormData();
    formData.append("file", file);

    const response = await fetch(`${API_BASE_URL}/api/v1/analyze/screenshot`, {
      method: "POST",
      body: formData,
      signal: controller.signal,
    });

    if (!response.ok) {
      const errorMsg = await parseErrorMessage(
        response,
        `Screenshot analysis request failed with status ${response.status}.`
      );
      throw new Error(errorMsg);
    }

    return await response.json();
  } catch (error: unknown) {
    if (error instanceof Error) {
      if (error.name === "AbortError") {
        throw new Error("The analysis request timed out. The server took too long to respond.");
      }
      if (
        error.message.includes("Failed to fetch") ||
        error.message.includes("NetworkError") ||
        error.message.includes("ECONNREFUSED")
      ) {
        throw new Error(
          `Cannot connect to the RakshaScan server at ${API_BASE_URL}. Please ensure the backend is running.`
        );
      }
      throw error;
    }
    throw new Error("An unexpected network error occurred while analyzing the screenshot.");
  } finally {
    clearTimeout(timeoutId);
  }
}

