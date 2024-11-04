import styles from './style.module.scss'

interface Props {
    hook: (value: string) => void
    value: string
}

export function Input({value, hook}: Props) {
    return <input className={styles['input']} type={'text'} value={value} onChange={e => hook(e.target.value)}/>
}