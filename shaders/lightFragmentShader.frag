#version 330

out vec4 outColor;

uniform vec4 color = vec4(1, 1, 1, 1);

void main()
{
   outColor = color;
}