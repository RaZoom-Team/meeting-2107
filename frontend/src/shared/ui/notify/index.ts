import { Store } from "react-notifications-component"

interface Props {
    title: string
    content: string
    type: "success" | "warning"
}

export function addNotify({title, content, type}: Props) {
    Store.addNotification({
        title: title,
        message: content,
        container: "top-center",
        type: type,
        dismiss: {
            duration: 2000,
            onScreen: true,
          },
    })
}