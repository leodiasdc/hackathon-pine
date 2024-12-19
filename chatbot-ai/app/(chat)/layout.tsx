import { cookies } from 'next/headers';

import { AppSidebar } from '@/components/app-sidebar';
import { SidebarInset, SidebarProvider } from '@/components/ui/sidebar';

import { auth } from '../(auth)/auth';
import { getUserById } from '@/lib/api/routes';

export const experimental_ppr = true;

export default async function Layout({
  children,
}: {
  children: React.ReactNode;
}) {
  const [cookieStore] = await Promise.all([cookies()]);
  const isCollapsed = cookieStore.get('sidebar:state')?.value !== 'true';
  let userId = cookieStore.get('userId')?.value
  console.log("myuserID")
  console.log(userId)
  let user = await getUserById({id: userId})
  console.log("myUser")
  console.log(user)
  
  return (
    <SidebarProvider defaultOpen={!isCollapsed}>
      <AppSidebar user={user} />
      <SidebarInset>{children}</SidebarInset>
    </SidebarProvider>
  );
}
