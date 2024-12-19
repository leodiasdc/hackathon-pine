import { cookies } from 'next/headers';

import { Chat } from '@/components/chat';
import { generateUUID } from '@/lib/utils';
import { redirect } from 'next/navigation';

export default async function Page() {
  const id = generateUUID();

  const cookieStore = await cookies();
  let token = cookieStore.get('token')?.value
  if (!token) {
    redirect('/login')
  }

  return (
    <Chat
      key={id}
      id={id}
      initialMessages={[]}
      isReadonly={false}
    />
  );
}
