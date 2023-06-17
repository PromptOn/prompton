/**
 * prompton-api
 * API for prompton - managing full lifecycle of AI chat prompts.
 *
 * The version of the OpenAPI document: 0.0.1
 * 
 *
 * NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).
 * https://openapi-generator.tech
 * Do not edit the class manually.
 */

import { RequestFile } from './models';
import { ChatGPTChatCompletitionConfig } from './chatGPTChatCompletitionConfig';
import { ChatGPTMessage } from './chatGPTMessage';
import { PromptVersionProviders } from './promptVersionProviders';
import { PromptVersionStatus } from './promptVersionStatus';

export class PromptVersionRead {
    'id'?: string;
    'createdAt'?: Date;
    'createdByUserId'?: string;
    'createdByOrgId'?: string;
    'status'?: PromptVersionStatus;
    'provider'?: PromptVersionProviders;
    'name': string;
    'description'?: string;
    'promptId': string;
    'template'?: Array<ChatGPTMessage>;
    'modelConfig'?: ChatGPTChatCompletitionConfig;
    'templateArgNames'?: Array<string>;

    static discriminator: string | undefined = undefined;

    static attributeTypeMap: Array<{name: string, baseName: string, type: string}> = [
        {
            "name": "id",
            "baseName": "_id",
            "type": "string"
        },
        {
            "name": "createdAt",
            "baseName": "created_at",
            "type": "Date"
        },
        {
            "name": "createdByUserId",
            "baseName": "created_by_user_id",
            "type": "string"
        },
        {
            "name": "createdByOrgId",
            "baseName": "created_by_org_id",
            "type": "string"
        },
        {
            "name": "status",
            "baseName": "status",
            "type": "PromptVersionStatus"
        },
        {
            "name": "provider",
            "baseName": "provider",
            "type": "PromptVersionProviders"
        },
        {
            "name": "name",
            "baseName": "name",
            "type": "string"
        },
        {
            "name": "description",
            "baseName": "description",
            "type": "string"
        },
        {
            "name": "promptId",
            "baseName": "prompt_id",
            "type": "string"
        },
        {
            "name": "template",
            "baseName": "template",
            "type": "Array<ChatGPTMessage>"
        },
        {
            "name": "modelConfig",
            "baseName": "model_config",
            "type": "ChatGPTChatCompletitionConfig"
        },
        {
            "name": "templateArgNames",
            "baseName": "template_arg_names",
            "type": "Array<string>"
        }    ];

    static getAttributeTypeMap() {
        return PromptVersionRead.attributeTypeMap;
    }
}

export namespace PromptVersionRead {
}