import { default as URLSearchParams } from "@ungap/url-search-params";
import { AxiosAdapter } from "axios";
import { APIResponse } from "./APIResponse";
export interface FetchFunction {
    (args: Fetcher.Args & {
        responseType?: "json";
    }): Promise<APIResponse<unknown, Fetcher.Error>>;
    (args: Fetcher.Args & {
        responseType: "blob";
    }): Promise<APIResponse<Blob, Fetcher.Error>>;
}
export declare namespace Fetcher {
    interface Args {
        url: string;
        method: string;
        contentType?: string;
        headers?: Record<string, string | undefined>;
        queryParameters?: URLSearchParams;
        body?: unknown;
        timeoutMs?: number;
        withCredentials?: boolean;
        responseType?: "json" | "blob";
        adapter?: AxiosAdapter;
        onUploadProgress?: (event: ProgressEvent) => void;
    }
    type Error = FailedStatusCodeError | NonJsonError | TimeoutError | UnknownError;
    interface FailedStatusCodeError {
        reason: "status-code";
        statusCode: number;
        body: unknown;
    }
    interface NonJsonError {
        reason: "non-json";
        statusCode: number;
        rawBody: string;
    }
    interface TimeoutError {
        reason: "timeout";
    }
    interface UnknownError {
        reason: "unknown";
        errorMessage: string;
    }
}
export declare const fetcher: FetchFunction;
