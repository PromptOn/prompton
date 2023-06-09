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
import { ChatGPTCompletitionChoice } from './chatGPTCompletitionChoice';
import { ChatGPTTokenUsage } from './chatGPTTokenUsage';

export class ChatGPTChatCompletitionResponse {
    'id': string;
    'object': string;
    'created': number;
    'model': string;
    'usage': ChatGPTTokenUsage;
    'choices': Array<ChatGPTCompletitionChoice>;

    static discriminator: string | undefined = undefined;

    static attributeTypeMap: Array<{name: string, baseName: string, type: string}> = [
        {
            "name": "id",
            "baseName": "id",
            "type": "string"
        },
        {
            "name": "object",
            "baseName": "object",
            "type": "string"
        },
        {
            "name": "created",
            "baseName": "created",
            "type": "number"
        },
        {
            "name": "model",
            "baseName": "model",
            "type": "string"
        },
        {
            "name": "usage",
            "baseName": "usage",
            "type": "ChatGPTTokenUsage"
        },
        {
            "name": "choices",
            "baseName": "choices",
            "type": "Array<ChatGPTCompletitionChoice>"
        }    ];

    static getAttributeTypeMap() {
        return ChatGPTChatCompletitionResponse.attributeTypeMap;
    }
}

