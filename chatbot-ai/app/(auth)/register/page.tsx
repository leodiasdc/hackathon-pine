'use client';

import Link from 'next/link';
import { useRouter } from 'next/navigation';
import { useActionState, useEffect, useState } from 'react';
import { toast } from 'sonner';
import  Image  from 'next/image';
import { AuthForm } from '@/components/auth-form';
import { SubmitButton } from '@/components/submit-button';

import { register, type RegisterActionState } from '../actions';

export default function Page() {
  const router = useRouter();

  const [email, setEmail] = useState('');
  const [isSuccessful, setIsSuccessful] = useState(false);

  const [state, formAction] = useActionState<RegisterActionState, FormData>(
    register,
    {
      status: 'idle',
    },
  );

  useEffect(() => {
    if (state.status === 'user_exists') {
      toast.error('Essa conta já existe.');
    } else if (state.status === 'failed') {
      toast.error('Falha em criar a conta.');
    } else if (state.status === 'invalid_data') {
      toast.error('Falha em validar sua submissão.');
    } else if (state.status === 'success') {
      toast.success('Conta criada com sucesso!');
      setIsSuccessful(true);
      router.refresh();
    }
  }, [state, router]);

  const handleSubmit = (formData: FormData) => {
    setEmail(formData.get('email') as string);
    formAction(formData);
  };

  return (
    <div className="flex h-dvh w-screen items-start pt-12 md:pt-0 md:items-center justify-center bg-background">
      <div className="w-full max-w-md overflow-hidden rounded-2xl gap-12 flex flex-col">
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
          <h3 className="text-xl font-semibold dark:text-zinc-50">Registrar</h3>
          <p className="text-sm text-white-500 dark:text-zinc-400">
            Cria uma conta com seu email e senha
          </p>
        </div>
        <AuthForm action={handleSubmit} defaultEmail={email}>
          <SubmitButton isSuccessful={isSuccessful}>Registrar</SubmitButton>
          <p className="text-center text-sm text-white-600 mt-4 dark:text-zinc-400">
            {'Você já possui uma conta? '}
            <Link
              href="/login"
              className="font-semibold text-white-800 hover:underline dark:text-zinc-200"
            >
              Entrar
            </Link>
            {' ao invés disso.'}
          </p>
        </AuthForm>
      </div>
    </div>
  );
}
