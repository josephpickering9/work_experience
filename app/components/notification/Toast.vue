<template>
  <div v-if="notification" class="alert" :class="typeClass">
    <span>{{ notification.message }}</span>
  </div>
</template>

<script setup lang="ts">
// Library imports
import { ref, computed, onMounted } from 'vue'
import { formatDistanceToNow } from 'date-fns'

// Local imports
import { NotificationType } from '../../../types/NotificationType'
import type { Notification } from '../../../types/Notification'
import { useNotificationStore } from '../../store/NotificationStore'

// Props
interface Props {
  notification?: Notification | null
}

const props = withDefaults(defineProps<Props>(), {
  notification: null,
})

// Refs
const createdAt = ref<Date | null>(new Date())
const timeSinceCreated = ref('Just now')

// Computed
const typeClass = computed((): string => {
  if (!props.notification) return 'alert-info'

  switch (props.notification.type) {
    case NotificationType.SUCCESS:
      return 'alert-success'
    case NotificationType.ERROR:
      return 'alert-error'
    case NotificationType.WARNING:
      return 'alert-warning'
    case NotificationType.INFO:
      return 'alert-info'
    default:
      return 'alert-info'
  }
})

// Methods
function close() {
  if (props.notification) {
    useNotificationStore().removeNotification(props.notification.id)
  }
}

// Lifecycle methods
onMounted(() => {
  if (!props.notification) return

  const thirtySeconds = 30 * 1000
  setTimeout(
    () => () =>
        setInterval(() => (timeSinceCreated.value = `${formatDistanceToNow(createdAt.value as Date)} ago`), thirtySeconds),
    thirtySeconds,
  )

  if (props.notification.seconds) {
    setTimeout(() => close(), props.notification.seconds * 1000)
  }
})
</script>
