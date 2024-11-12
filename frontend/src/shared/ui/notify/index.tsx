import { Button, Text } from "@gravity-ui/uikit"
import styles from './styles.module.scss'
import ReactDOMClient from 'react-dom/client';
import {Toaster} from '@gravity-ui/uikit';

Toaster.injectReactDOMClient(ReactDOMClient);
const toaster = new Toaster({mobile: true});

interface Props {
    title: string
    content: string
    type?: "success" | "normal" | "info" | "warning" | "danger" | "utility" | undefined
}

export function AddNotify({title, content, type}: Props) {
    const contentToaster = <div className={styles['toaster-container']}>
    <Text variant="body-1">{content}</Text>
    <Button size='l' onClick={() => toaster.remove(title)}>Понятно</Button>
    </div>

    toaster.add({
        title: title,
        name: title,
        content: contentToaster,
        theme: (type ? type : 'success')
    })
}