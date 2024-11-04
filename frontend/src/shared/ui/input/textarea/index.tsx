import styles from './style.module.scss'

interface Props {
    value: string
    hook: (value: string) => void
}

export function TextArea({value, hook}: Props) {
    return <textarea value={value} onChange={e => hook(e.target.value)} className={styles['textarea']}></textarea>
}