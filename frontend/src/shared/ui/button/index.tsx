import styles from './style.module.scss'

interface Props {
    text: string
    hook: () => void
    active: boolean
    style?: 'fill' | 'outfill'
}

export function Button({text, hook, active, style}: Props) {
    return <button disabled={!active} data-active={active ? "YES" : "NO"} data-style={style || 'fill'} className={styles['button']} onClick={hook}>{text}</button>
}