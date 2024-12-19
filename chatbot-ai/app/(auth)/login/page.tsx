'use client';

import Link from 'next/link';
import { redirect, useRouter } from 'next/navigation';
import { useActionState, useEffect, useState } from 'react';
import { toast } from 'sonner';
import Image from 'next/image';
import { AuthForm } from '@/components/auth-form';
import { SubmitButton } from '@/components/submit-button';

import { login, type LoginActionState } from '../actions';

export default function Page() {

  const router = useRouter();

  const [email, setEmail] = useState('');
  const [isSuccessful, setIsSuccessful] = useState(false);

  const handleSubmit = (formData: FormData) => {
    const url = `${process.env.NEXT_PUBLIC_BASE_URL}/api/login`;
    const options = {
      method: "POST",
      headers: {
          Accept: "application/json",
          "Content-Type": "application/json;charset=UTF-8",
          "Authorization": 'Basic ' + btoa(formData.get('email') + ":" + formData.get("password")),
      }
    };
    console.log("options")
    console.log(options)
    fetch(url, options)
      .then((res) => res.json())
      .then( (data) => {
        console.log(data)
        if (data.error) {
          toast.error("Falha no login")
          return
        }
        let token = data.token
        let userId = data.userId
        document.cookie = `token=${token}`;
        document.cookie = `userId=${userId}`;
      })
      .then(() => {
        router.replace("/")
      });
    //setEmail(formData.get('email') as string);
    //formAction(formData);
  };

  return (
    <div className="flex h-dvh w-screen items-start pt-12 md:pt-0 md:items-center justify-center bg-background">
      <div className="w-full max-w-md overflow-hidden rounded-2xl flex flex-col gap-12">
        <div className="flex flex-col items-center justify-center gap-2 px-4 text-center sm:px-16">
          <p className="flex flex-row justify-center gap-4 items-center">
            <Image
              src="/images/banco_pine.jpg"
              alt="Logo do BancoPine" 
              width={100}
              height={100}
              className="squared-full"
            />
          </p>
          <h3 className="text-xl font-semibold dark:text-zinc-50">Entrar</h3>
          <p className="text-sm text-white-500 dark:text-zinc-400">
            Use seu email e senha para entrar
          </p>
        </div>
        <AuthForm action={handleSubmit} defaultEmail={email}>
          <SubmitButton isSuccessful={isSuccessful}>Entrar</SubmitButton>
          <p className="text-center text-sm text-white-600 mt-4 dark:text-zinc-400">
            {"Não possui uma conta? "}
            <Link
              href="/register"
              className="font-semibold text-white-800 hover:underline dark:text-zinc-200"
            >
              Registre
            </Link>
            {' de graça.'}
          </p>
        </AuthForm>
      </div>
    </div>
  );
}
