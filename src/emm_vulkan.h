#ifndef EMM_VULKAN_H
#define EMM_VULKAN_H

#include <vulkan/vulkan.h>
#include <stdlib.h>
#include <string.h>
#include "intdef.h"

// SDL is not included
// SDL details need to be filled out outside of here
// This way this glfw could be dropped in for free

typedef struct VulkanApp {
	// leave all these as VK_NULL_HANDLEs
	VkInstance instance;
	VkPhysicalDevice physicalDevice;
	VkDevice device;	
	VkSurfaceKHR surface;
	VkDebugUtilsMessengerEXT debugMessenger;

	// fill this out with the number of queues you need
	uint32 queueCount;
	
	// fill this out with the extensions you need from an instance
	const char **extensionNames;
	uint32 extensionCount;
	
	// fill this out with the extensions you need from a physical device
	const char **deviceExtensionNames;
	uint32 deviceExtensionCount;

	// assign this to the address of a callback function for debug info. Or leave as NULL to disable.
	PFN_vkDebugUtilsMessengerCallbackEXT debugCallbackFunction;

	VkAllocationCallbacks *allocator;
	// fill this with app name
	const char *name;
	// enable validation ?
	bool validate;
} VulkanApp;

VkResult initializeVulkanApp(VulkanApp *app);
void quitVulkanApp(VulkanApp *app);

#endif
