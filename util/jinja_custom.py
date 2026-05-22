from fastapi.templating import Jinja2Templates

class CorrecaoJinjaTemplates(Jinja2Templates):
    def TemplateResponse(self, *args, **kwargs):
        # Se o primeiro argumento posicional for uma string (padrão antigo: "template.html", {...})
        if args and isinstance(args[0], str):
            name = args[0]
            context = args[1] if len(args) > 1 else kwargs.get("context", {})
            request = context.pop("request", None)
            
            if request:
                kwargs["request"] = request
                kwargs["name"] = name
                kwargs["context"] = context
                return super().TemplateResponse(**kwargs)
                
        return super().TemplateResponse(*args, **kwargs)