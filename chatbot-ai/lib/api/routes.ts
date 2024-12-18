export async function getChatById({ id }: { id: string }) {
    try {
        const url = `${process.env.NEXT_PUBLIC_BASE_URL}/api/chat/${id}`;
        const options = {
        method: "GET",
        headers: {
            Accept: "application/json",
            "Content-Type": "application/json;charset=UTF-8",
        }
        };
        fetch(url, options)
        .then((response) => response.json())
        .then((data) => {
            console.log(data);
        });
      return selectedChat;
    } catch (error) {
      console.error('Failed to get chat by id from database');
      throw error;
    }
  }


  export async function getMessagesByChatId({ id }: { id: string }) {
    try {
      return await db
        .select()
        .from(message)
        .where(eq(message.chatId, id))
        .orderBy(asc(message.createdAt));
    } catch (error) {
      console.error('Failed to get messages by chat id from database', error);
      throw error;
    }
  }
  