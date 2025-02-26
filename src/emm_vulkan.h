#ifndef EMM_VULKAN_H
#define EMM_VULKAN_H

#include <vulkan/vulkan.h>
#include <stdlib.h>
#include <string.h>
#include "intdef.h"

typedef struct VulkanApp {
	VkInstance instance;
	VkPhysicalDevice physicalDevice;
	VkDevice device;	


	uint32 queueCount; // if greater than zero, select a queue family with at least that many queues
	
	const char **extensionNames;
	uint32 extensionCount;

	PFN_vkDebugUtilsMessengerCallbackEXT debugCallbackFunction;
	VkDebugUtilsMessengerEXT debugMessenger;

	
	VkAllocationCallbacks *allocator;
	const char *name;
	bool validate;
} VulkanApp;

VkResult initializeVulkanApp(VulkanApp *app);
void quitVulkanApp(VulkanApp *app);

#endif
