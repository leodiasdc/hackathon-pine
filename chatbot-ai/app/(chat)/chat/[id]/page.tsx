import { cookies } from 'next/headers';
import { notFound } from 'next/navigation';

import { Chat } from '@/components/chat';
//import { getChatById, getMessagesByChatId } from '@/lib/db/queries';
import { getChatById, getMessagesByChatId } from '@/lib/api/routes';
import { convertToUIMessages } from '@/lib/utils';

export default async function Page(props: { params: Promise<{ id: string }> }) {
  const params = await props.params;
  const { id } = params;
  const chat = await getChatById({ id });
  console.log("chat")
  console.log(chat)

  if (!chat) {
    console.log("chat não encontrado")
    notFound();
  }
  console.log("chat encontrado")

  //const session = await auth();
  const cookieStore = await cookies();
  let userId = cookieStore.get('userId')?.value

  if (chat.visibility === 'private') {
    /*
    if (!session || !session.user) {
      return notFound();
    }
    */
    if (userId !== chat.userId) {
      return notFound();
    }
  }

  const messagesFromDb = await getMessagesByChatId({
    id,
  });

  return (
    <Chat
      id={chat.id}
      initialMessages={convertToUIMessages(messagesFromDb)}
      isReadonly={userId !== chat.userId}
    />
  );
}
