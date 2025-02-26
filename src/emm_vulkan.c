#include "emm_vulkan.h"

VkResult initializeVulkanApp(VulkanApp *app) {
	VkResult res;

	// step one : create instance 

	VkApplicationInfo applicationInfo = {
		.sType = VK_STRUCTURE_TYPE_APPLICATION_INFO,
		.pApplicationName = app->name,
		.pEngineName = app->name,
		.apiVersion = VK_API_VERSION_1_3
	};

	VkInstanceCreateInfo instanceCreateInfo = {
		.sType = VK_STRUCTURE_TYPE_INSTANCE_CREATE_INFO,
		.flags = VK_INSTANCE_CREATE_ENUMERATE_PORTABILITY_BIT_KHR,
		.pApplicationInfo = &applicationInfo,
		.enabledExtensionCount = app->extensionCount,
		.ppEnabledExtensionNames = app->extensionNames
	};
	const char *validationLayerNames[] = {
		"VK_LAYER_KHRONOS_validation"
	};

	if (app->validate) {
		// todo check layer availibility and only enable if they are availible
		instanceCreateInfo.enabledLayerCount = 1;
		instanceCreateInfo.ppEnabledLayerNames = validationLayerNames;
	}

	res = vkCreateInstance(&instanceCreateInfo, app->allocator, &app->instance);
	
	if (res != VK_SUCCESS) {
		return res;
	}

	if (app->validate && app->debugCallbackFunction) {
		// register the debug messenger function
		VkDebugUtilsMessengerCreateInfoEXT debugMessengerCreateInfo = {
			.sType = VK_STRUCTURE_TYPE_DEBUG_UTILS_MESSENGER_CREATE_INFO_EXT,
			.messageSeverity = VK_DEBUG_UTILS_MESSAGE_SEVERITY_VERBOSE_BIT_EXT, 
			.messageType = VK_DEBUG_UTILS_MESSAGE_TYPE_GENERAL_BIT_EXT |
						   VK_DEBUG_UTILS_MESSAGE_TYPE_VALIDATION_BIT_EXT | 
						   VK_DEBUG_UTILS_MESSAGE_TYPE_PERFORMANCE_BIT_EXT,
			.pfnUserCallback = app->debugCallbackFunction 
		};

		PFN_vkCreateDebugUtilsMessengerEXT vkCreateDebugUtilsMessengerEXT =
			(PFN_vkCreateDebugUtilsMessengerEXT) vkGetInstanceProcAddr(
			app->instance, "vkCreateDebugUtilsMessengerEXT");
		
		vkCreateDebugUtilsMessengerEXT(app->instance, &debugMessengerCreateInfo, 
									   app->allocator, &app->debugMessenger);
	}

	// step two : choose a physical device

	uint32 physicalDeviceCount;
	vkEnumeratePhysicalDevices(app->instance, &physicalDeviceCount, NULL);
	VkPhysicalDevice *physicalDevices = malloc(sizeof(VkPhysicalDevice) * physicalDeviceCount);
	if (physicalDevices == NULL) return VK_ERROR_OUT_OF_HOST_MEMORY;
	vkEnumeratePhysicalDevices(app->instance, &physicalDeviceCount, physicalDevices);

	// select the first physical device that has a queueFamily with graphics operations
	uint32 queueFamilyCount = 0, queueFamilyIndex;
	VkQueueFamilyProperties *queueFamilyProperties;
	VkQueueFlags requiredQueueFlags = VK_QUEUE_GRAPHICS_BIT;

	for (uint32 i = 0; i < physicalDeviceCount; i++) {
		vkGetPhysicalDeviceQueueFamilyProperties(physicalDevices[i], &queueFamilyCount, NULL);
		queueFamilyProperties = malloc(sizeof(VkQueueFamilyProperties) * queueFamilyCount);
		if (queueFamilyProperties == NULL) return VK_ERROR_OUT_OF_HOST_MEMORY;
		vkGetPhysicalDeviceQueueFamilyProperties(physicalDevices[i], &queueFamilyCount, 
			queueFamilyProperties);
		for (uint32 j = 0; j < queueFamilyCount; j++) {
			if ((queueFamilyProperties[i].queueFlags & requiredQueueFlags)) {
				// does the queue family contain at lease the requested number of queues
				if (app->queueCount == 0 || app->queueCount >= queueFamilyProperties[i].queueCount) {
					if (app->queueCount == 0) app->queueCount = queueFamilyProperties[i].queueCount;
					queueFamilyIndex = j;
					app->physicalDevice = physicalDevices[i];
					break;
				}
			}
		}
		free(queueFamilyProperties);
		if (app->physicalDevice != VK_NULL_HANDLE) break;
	}

	
	if (app->physicalDevice == VK_NULL_HANDLE) return VK_ERROR_FEATURE_NOT_PRESENT;
	
	free(physicalDevices);

	// step three : create logical device
	float *queuePriorities = malloc(sizeof(float) * app->queueCount);
	if (queuePriorities == NULL) return VK_ERROR_OUT_OF_HOST_MEMORY;
	for (uint32 i = 0; i < app->queueCount; i++) {
		queuePriorities[i] = 1.0f / app->queueCount;
	}

	VkDeviceQueueCreateInfo deviceQueueCreateInfo = {
		.sType = VK_STRUCTURE_TYPE_DEVICE_QUEUE_CREATE_INFO,
		.queueFamilyIndex = queueFamilyIndex,
		.queueCount = app->queueCount,
		.pQueuePriorities = queuePriorities 
	};

	VkDeviceCreateInfo deviceCreateInfo = {
		.sType = VK_STRUCTURE_TYPE_DEVICE_CREATE_INFO,
		.queueCreateInfoCount = 1,
		.pQueueCreateInfos = &deviceQueueCreateInfo,
		.enabledExtensionCount = 0,
		.ppEnabledExtensionNames = NULL,
	};
	
	res = vkCreateDevice(app->physicalDevice, &deviceCreateInfo, app->allocator, &app->device);

	free(queuePriorities);

	if (res != VK_SUCCESS) return res;

	return VK_SUCCESS;
}

void quitVulkanApp(VulkanApp *app) {
	if (app == NULL || app->instance == VK_NULL_HANDLE) return;

	if (app->debugMessenger != VK_NULL_HANDLE) {
		PFN_vkDestroyDebugUtilsMessengerEXT vkDestroyDebugUtilsMessengerEXT =
			(PFN_vkDestroyDebugUtilsMessengerEXT) vkGetInstanceProcAddr(
			app->instance, "vkDestroyDebugUtilsMessengerEXT");
		vkDestroyDebugUtilsMessengerEXT(app->instance, app->debugMessenger, app->allocator);
	}
	if (app->device != VK_NULL_HANDLE) {
		vkDestroyDevice(app->device, app->allocator);
	}
	vkDestroyInstance(app->instance, app->allocator);
}
