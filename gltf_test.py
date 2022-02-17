from pygltflib import GLTF2

filename = "public/testthreejs.gltf"
gltf = GLTF2().load(filename)
print (gltf)

current_scene = gltf.scenes[gltf.scene]
print ('Scene:', current_scene)
#print ('Node:', gltf.nodes)
for node in gltf.nodes:
    print ('Node:', node)

print("Mesh:", gltf.meshes[0])

if __name__ == '__main__':
    print("Gltf lecture")
