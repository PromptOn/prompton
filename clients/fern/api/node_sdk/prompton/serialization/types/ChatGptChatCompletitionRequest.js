"use strict";
/**
 * This file was auto-generated by Fern from our API Definition.
 */
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    var desc = Object.getOwnPropertyDescriptor(m, k);
    if (!desc || ("get" in desc ? !m.__esModule : desc.writable || desc.configurable)) {
      desc = { enumerable: true, get: function() { return m[k]; } };
    }
    Object.defineProperty(o, k2, desc);
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || function (mod) {
    if (mod && mod.__esModule) return mod;
    var result = {};
    if (mod != null) for (var k in mod) if (k !== "default" && Object.prototype.hasOwnProperty.call(mod, k)) __createBinding(result, mod, k);
    __setModuleDefault(result, mod);
    return result;
};
var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.ChatGptChatCompletitionRequest = void 0;
const core = __importStar(require("../../core"));
exports.ChatGptChatCompletitionRequest = core.serialization.object({
    model: core.serialization.string().optional(),
    temperature: core.serialization.number().optional(),
    topP: core.serialization.property("top_p", core.serialization.number().optional()),
    stop: core.serialization.lazy(() => __awaiter(void 0, void 0, void 0, function* () { return (yield Promise.resolve().then(() => __importStar(require("..")))).ChatGptChatCompletitionRequestStop; })).optional(),
    maxTokens: core.serialization.property("max_tokens", core.serialization.number().optional()),
    presencePenalty: core.serialization.property("presence_penalty", core.serialization.number().optional()),
    frequencyPenalty: core.serialization.property("frequency_penalty", core.serialization.number().optional()),
    logitBias: core.serialization.property("logit_bias", core.serialization.record(core.serialization.string(), core.serialization.number()).optional()),
    messages: core.serialization.list(core.serialization.lazyObject(() => __awaiter(void 0, void 0, void 0, function* () { return (yield Promise.resolve().then(() => __importStar(require("..")))).ChatGptMessage; }))),
    n: core.serialization.number().optional(),
    stream: core.serialization.boolean().optional(),
    user: core.serialization.string().optional(),
});