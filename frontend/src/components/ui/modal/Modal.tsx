'use client'

import React, { ReactNode } from 'react'
import styles from './Modal.module.scss'

interface ModalProps {
  children: ReactNode,
  isOpen: boolean,
  onClose: () => void
}

const Modal = ({ children, isOpen, onClose }: ModalProps) => {
  if (!isOpen) return null

  const handleClose = () => {
    onClose()
  }

  return (
    <div className={styles.modal} onClick={() => handleClose()}>
      <div className={styles.modalContent} onClick={e => e.stopPropagation()}>{children}</div>
    </div>
  )
}

export default Modal