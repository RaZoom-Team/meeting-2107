import styles from './style.module.scss'
import { useContext, useEffect, useState} from 'react'
import {Auth} from '../../pages'
import { UserContext } from '../providers'
import { editIcon, feedIcon, historyIcon, NavBar, NavIcon } from '../../shared'
import { Router } from '../router/router'
import { Loader } from '@gravity-ui/uikit'
import ReactDOMClient from 'react-dom/client';
import {Toaster} from '@gravity-ui/uikit';

export type Page = 'feed' | 'history' | 'edit'
Toaster.injectReactDOMClient(ReactDOMClient);

export function App() {
  const {user} = useContext(UserContext)
  const [page, setPage] = useState<Page>('feed')

  useEffect(() => {
    Telegram.WebApp.expand()
  }, [])

  if (user === undefined) {
    return <main className={styles['main']}>
      <Loader size='l'></Loader>
    </main>
  } 
  else if (user === null) {
    return <Auth/>
  } 
  else {

    const buttons: NavIcon[] = [
      {src: editIcon, hook: () => setPage('edit'), active: page == 'edit'},
      {src: feedIcon, hook: () => setPage('feed'), active: page == 'feed'},
      {src: historyIcon, hook: () => setPage('history'), active: page == 'history'},
    ]

    return  <main data-theme={user.male ? 'blue' : 'pink'} className={styles['main']}>
        <NavBar buttons={buttons}/>
        <Router page={page} focus={user.focus_user}/>
    </main>

  }
}

