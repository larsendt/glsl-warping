uniform float screen;

void main()
{
   gl_Position = gl_ModelViewProjectionMatrix * gl_Vertex;
   gl_TexCoord[0] = vec4(gl_Position.x * screen, gl_Position.y, 1.0, 1.0);
}
