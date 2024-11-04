import { Sex } from '../../../pages/auth/model/types'
import styles from './style.module.scss'

export type Option = {
    key: string
    value: string
}

interface Props {
    value: string
    options: Option[]
    title: string
    hook: (value: string | Sex) => void
}

export function Select({value, options, hook, title}: Props) {
    return <select value={value} className={styles['select']} defaultValue={title} onChange={(e) => hook(e.target.value)}>
        <option value={''} selected hidden disabled>{title}</option>
        {options.map((option: Option) => <option key={option.key} value={option.value}>{option.value}</option>)}
    </select>
}