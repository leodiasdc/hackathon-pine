'use server';

import { cookies } from 'next/headers';
import { getCookie } from '@/lib/utils'
import type { Message as DBMessage } from '@/lib/db/schema';

export async function getChatById({ id }: { id: string }) {
  try {
    const cookieStore = await cookies();
    let token = cookieStore.get("token")?.value
    const url = `${process.env.NEXT_PUBLIC_BASE_URL}/api/chat/${id}`;
    const options = {
    method: "GET",
    headers: {
        Accept: "application/json",
        "Content-Type": "application/json;charset=UTF-8",
        "Authorization": 'Bearer ' + token
    }
    };
    const response = await fetch(url, options)
    return await response.json();
  } catch (error) {
    console.error('Failed to get chat by id from database');
    throw error;
  }
}

export async function getMessagesByChatId({ id }: { id: string }) {
  try {
    const cookieStore = await cookies();
    let token = cookieStore.get("token")?.value
    const url = `${process.env.NEXT_PUBLIC_BASE_URL}/api/messages/${id}`;
    const options = {
    method: "GET",
    headers: {
        Accept: "application/json",
        "Content-Type": "application/json;charset=UTF-8",
        "Authorization": 'Bearer ' + token
    }
    };
    const response = await fetch(url, options)
    return await response.json();
  } catch (error) {
    console.error('Failed to get messages by chat id from database', error);
    throw error;
  }
}

export async function getUserById({ id }: { id: string | undefined}) {
  if (id == undefined) {
    return id
  }
  const cookieStore = await cookies();
  let token = cookieStore.get("token")?.value
  try {
    const url = `${process.env.NEXT_PUBLIC_BASE_URL}/api/user/${id}`;
    const options = {
    method: "GET",
    headers: {
        Accept: "application/json",
        "Content-Type": "application/json;charset=UTF-8",
        "Authorization": 'Bearer ' + token
    }
    };
    console.log("options")
    console.log(options)
    const response = await fetch(url, options);
    return await response.json();
  } catch (error) {
    console.error('Failed to get messages by chat id from database', error);
    throw error;
  }
}

export async function sendPrompt(message: DBMessage) {
  const cookieStore = await cookies();
  let token = cookieStore.get("token")?.value
  let data = message;
  try {
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
    console.log("options")
    console.log(options)
    const response = await fetch(url, options);
    console.log(response)
    return await response.json();
  } catch (error) {
    console.error('Failed to send message', error);
    throw error;
  }
}