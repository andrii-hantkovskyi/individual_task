import { bindActionCreators } from 'redux'
import { RootAction } from '@/store/root-action'
import { useDispatch } from 'react-redux'

export const useActions = () => {
  const dispatch = useDispatch()
  return bindActionCreators(RootAction, dispatch)
}