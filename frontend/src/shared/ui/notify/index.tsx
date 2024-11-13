import { Button, Text } from "@gravity-ui/uikit"
import styles from './styles.module.scss'
import ReactDOMClient from 'react-dom/client';
import {Toaster} from '@gravity-ui/uikit';

Toaster.injectReactDOMClient(ReactDOMClient);
const toaster = new Toaster({mobile: true});

interface Props {
    title: string
    content: string
    type?: "success" | "normal" | "info" | "warning" | "danger" | "utility"
    btn_text?: string
    btn_hook?: () => void
}

export function addNotify({title, content, type, btn_text, btn_hook}: Props) {

    const action = btn_hook ? btn_hook : () => toaster.remove(title)

    const contentToaster = <div className={styles['toaster-container']}>
    <Text variant="body-1">{content}</Text>
    <Button size='l' onClick={action}>{btn_text ? btn_text : "Понятно"}</Button>
    </div>

    toaster.add({
        title: title,
        name: title,
        content: contentToaster,
        theme: (type ? type : 'success')
    })
}