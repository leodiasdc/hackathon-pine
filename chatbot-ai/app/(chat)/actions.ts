'use server';

import { type CoreUserMessage, generateText } from 'ai';
import { cookies } from 'next/headers';
import {createOpenAI} from "@ai-sdk/openai";
//import { customModel } from '@/lib/ai';
import {
  deleteMessagesByChatIdAfterTimestamp,
  getMessageById,
  updateChatVisiblityById,
} from '@/lib/db/queries';
import { VisibilityType } from '@/components/visibility-selector';
import { GitPullRequestClosed } from 'lucide-react';

export async function saveModelId(model: string) {
  const cookieStore = await cookies();
  cookieStore.set('model-id', model);
}

export async function generateTitleFromUserMessage({
  message,
}: {
  message: CoreUserMessage;
}) {
  const groq = createOpenAI({
    baseURL: "https://api.groq.com/openai/v1",
    apiKey: process.env.GROQ_API_KEY,
  });
  
  const { text: title } = await generateText({
    model: groq("llama3-8b-8192"),
    system: `\n
    Você vai gerar um título curto com base na primeira mensagem que o usuário começar uma conversa
    certifique-se de que não tenha mais de 40 caracteres
    o título deve ser um resumo da mensagem do usuário
    não use aspas nem dois-pontos. Lembre-se que você é o ChatBot do Banco Pine, o PineBot, que está auxiliando um cliente em suas tarefas e respondendo perguntas sobre a empresa.`,
    prompt: JSON.stringify(message),
  });

  return title;
}

export async function deleteTrailingMessages({ id }: { id: string }) {
  const [message] = await getMessageById({ id });

  await deleteMessagesByChatIdAfterTimestamp({
    chatId: message.chatId,
    timestamp: message.createdAt,
  });
}

export async function updateChatVisibility({
  chatId,
  visibility,
}: {
  chatId: string;
  visibility: VisibilityType;
}) {
  await updateChatVisiblityById({ chatId, visibility });
}
