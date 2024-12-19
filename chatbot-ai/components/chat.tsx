'use client';

import type { Attachment, Message } from 'ai';
import { useChat } from 'ai/react';
import { AnimatePresence } from 'framer-motion';
import { useState } from 'react';
import useSWR, { useSWRConfig } from 'swr';
import { useWindowSize } from 'usehooks-ts';
import type { Message as DBMessage, Vote } from '@/lib/db/schema';

import { ChatHeader } from '@/components/chat-header';
import { convertToUIMessages, fetcher, generateUUID, getCookie } from '@/lib/utils';

import { Block, type UIBlock } from './block';
import { BlockStreamHandler } from './block-stream-handler';
import { MultimodalInput } from './multimodal-input';
import { Messages } from './messages';
//import { sendPrompt } from '@/lib/api/routes';
import { useRouter } from 'next/navigation';

export function Chat({
  id,
  initialMessages,
  isReadonly,
}: {
  id: string;
  initialMessages: Array<Message>;
  isReadonly: boolean;
}) {
  const { mutate } = useSWRConfig();

  const {
    messages,
    setMessages,
    handleSubmit,
    input,
    setInput,
    append,
    isLoading,
    stop,
    reload,
    data: streamingData,
  } = useChat({
    id,
    body: { id },
    initialMessages,
    onFinish: () => {
      mutate(`${process.env.NEXT_PUBLIC_BASE_URL}/api/history`);
    },
  });

  const { width: windowWidth = 1920, height: windowHeight = 1080 } =
    useWindowSize();

  const [block, setBlock] = useState<UIBlock>({
    documentId: 'init',
    content: '',
    title: '',
    status: 'idle',
    isVisible: false,
    boundingBox: {
      top: windowHeight / 4,
      left: windowWidth / 4,
      width: 250,
      height: 50,
    },
  });

  //console.log("env:")
  //console.log(process.env.NEXT_PUBLIC_BASE_URL)
  let url = process.env.NEXT_PUBLIC_BASE_URL
  //console.log("let: " + url)

  const { data: votes } = useSWR<Array<Vote>>(
    `${process.env.NEXT_PUBLIC_BASE_URL}/api/vote?chatId=${id}`,
    fetcher,
  );

  const router = useRouter();

  const newHandleSubmit = () => {
    let messagePrompt : DBMessage = {
      id: generateUUID(),
      createdAt: new Date(),
      chatId: id,
      role: "user",
      content: input, 
    };

    let token = getCookie("token");
    let userId = getCookie("userId");
    let data = {
      "userId": userId,
      "message": messagePrompt
    }
    const url = `${process.env.NEXT_PUBLIC_BASE_URL}/api/chat/prompt`;
    const options = {
      method: "POST",
      body: JSON.stringify(data),
      headers: {
          Accept: "application/json",
          "Content-Type": "application/json;charset=UTF-8",
          "Authorization": 'Bearer ' + token
      }
    };

    let x = convertToUIMessages([messagePrompt]);
    messages.push(x[0]);
    setMessages(messages)
    //handleSubmit()

    console.log("options")
    console.log(options)
    fetch(url, options)
    .then((response) => response.json())
    .then((dataJson) => {
      console.log(dataJson)
      let data = dataJson.message;
      let messageResponse : DBMessage = {
        id: data.id,
        createdAt: data.createdAt,
        chatId: data.chatId,
        role: data.role,
        content: data.content
      }; 
      let array = [];
      array.push(messageResponse);
      let x = convertToUIMessages(array);
      messages.push(x[0]);
      console.log("setting messages")
      router.refresh();
    });
    /*
    let response = sendPrompt(messagePrompt);
    
    //let response = "olá response"

    console.log(response)
    let data = response.message;
    let messageResponse : DBMessage = {
      id: data.id,
      createdAt: data.createdAt,
      chatId: data.chatId,
      role: data.role,
      content: data.content
     }; 
     let array = [];
     array.push(messagePrompt);
     array.push(messageResponse);
     let x = convertToUIMessages(array);
     messages.push(x[0]);
     messages.push(x[1]);
     setMessages(messages);
     */
  }

  const [attachments, setAttachments] = useState<Array<Attachment>>([]);

  return (
    <>
      <div className="flex flex-col min-w-0 h-dvh bg-background">
        <ChatHeader
          chatId={id}
          isReadonly={isReadonly}
        />

        <Messages
          chatId={id}
          block={block}
          setBlock={setBlock}
          isLoading={isLoading}
          votes={votes}
          messages={messages}
          setMessages={setMessages}
          reload={reload}
          isReadonly={isReadonly}
        />

        <form className="flex mx-auto px-4 bg-background pb-4 md:pb-6 gap-2 w-full md:max-w-3xl">
          {!isReadonly && (
            <MultimodalInput
              chatId={id}
              input={input}
              setInput={setInput}
              handleSubmit={newHandleSubmit}
              isLoading={isLoading}
              stop={stop}
              attachments={attachments}
              setAttachments={setAttachments}
              messages={messages}
              setMessages={setMessages}
              append={append}
            />
          )}
        </form>
      </div>

      <AnimatePresence>
        {block?.isVisible && (
          <Block
            chatId={id}
            input={input}
            setInput={setInput}
            handleSubmit={newHandleSubmit}
            isLoading={isLoading}
            stop={stop}
            attachments={attachments}
            setAttachments={setAttachments}
            append={append}
            block={block}
            setBlock={setBlock}
            messages={messages}
            setMessages={setMessages}
            reload={reload}
            votes={votes}
            isReadonly={isReadonly}
          />
        )}
      </AnimatePresence>

      <BlockStreamHandler streamingData={streamingData} setBlock={setBlock} />
    </>
  );
}
